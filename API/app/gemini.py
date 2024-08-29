import os
import json
import time
import vertexai.preview.generative_models as generative_models

from vertexai.generative_models import GenerativeModel, Part

from datetime import datetime

from app import app

from config import Config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = Config.GOOGLE_APPLICATION_CREDENTIALS

class Gemini():
    def __init__(self):
        # LLM initialization
        self.model = Config.GEMINI_MODEL
        self.temperature = Config.GEMINI_TEMPERATURE
        self.max_tkns = Config.GEMINI_MAX_TOKENS
        self.top_p = Config.GEMINI_TOP_P

        self.llm = self.initialize_gemini()
    
    def initialize_gemini(self):
        safety_settings = {generative_models.HarmCategory.HARM_CATEGORY_UNSPECIFIED: generative_models.HarmBlockThreshold.BLOCK_NONE,
                           generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
                           generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
                           generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
                           generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE}
        
        model = GenerativeModel(self.model,
                                generation_config = {"temperature": self.temperature,
                                                     "max_output_tokens": self.max_tkns,
                                                     "top_p": self.top_p},
                                safety_settings = safety_settings)
        # print('LLM initialized')
        return model
    
    def create_doc(self, path:str):
        """Formats the document from Cloud Storage so the LLM can read it
        Inputs:
            - path: The url of the document in cloud storage"""
        
        doc = Part.from_uri(path,
                            mime_type = "application/pdf")

        # print('Document retrieved')
        return doc
    
    def clean_json(self, json_str):
        start = json_str.find('{')
        end = json_str.rfind('}')
        json_str = json_str[start:end+1]
        return json_str
    
    def retry_llm_response(self, msg):
        tries = 1
        chat = self.llm.start_chat(response_validation = False)

        while tries <= Config.GEMINI_LLM_RETRIES:
            try:
                response = chat.send_message(msg)
                ans = json.loads(self.clean_json(response.text))
                return ans
            
            except Exception as error:
                app.logger.error(f"{type(error).__name__}: {error}")
                print(f"LLM try {tries} out of {Config.GEMINI_LLM_RETRIES} failed. Trying again in {tries*10} seconds.")
                time.sleep(tries*10)
                tries += 1
        
        raise Exception("LLM generation out of tries. Manual data ingestion is required")
    
    def llm_call(self, query:str, path:str, pubmed_uuid:str, pubmed_docId:str):
        # Prepare the document
        doc = self.create_doc(path)
        msg = [doc, query]

        # Generate the LLM answer
        ans = self.retry_llm_response(msg)

        # print(ans["DOI"])
        # Remove http from DOI if exists
        if 'http' in ans["DOI"]:
            ans["DOI"] = ans["DOI"].split('doi.org/')[1]
        # print(ans["DOI"])

        # Generate metadata for the document
        ans['CreatedDate'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        ans['CreatedBy'] = 'SafetyVerse'
        ans['ModifiedDate'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        ans['ModifiedBy'] = 'SafetyVerse'
        ans['PubmedDoc_Id'] = pubmed_docId
        ans['Pubmed_UUID'] = pubmed_uuid
        ans['Type'] = 'Publication'
        ans['is_active'] = 1
        
        print(ans)
        return ans