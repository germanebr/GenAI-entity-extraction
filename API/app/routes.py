from flask import request

from app import app, prompts
from app.gemini import Gemini
from app.cloudSQL import CloudSQL

@app.route("/api/health")
def home():
    return ({"message": "connected successfully"})

@app.route("/run_pubmed", methods=['POST'])
def run_pubmed():
    app.logger.info("Executing Pubmed process")
    
    pubmed_uuid: str = request.json['pubmed_uuid']
    pubmed_docId: str = request.json['pubmed_docId']
    path: str = request.json['path']

    llm = Gemini()
    
    try:
        response = llm.llm_call(query = prompts.PUBMED_PROMPT,
                                path = path,
                                pubmed_uuid = pubmed_uuid,
                                pubmed_docId = pubmed_docId)
        # print("Got LLM response")
        # print(response)

        # Store only if the file is not on Cloud SQL already
        if not CloudSQL.get_existence({"DOI": response["DOI"]}):
            CloudSQL.insertWithParameters(response)
            # print("Saved the data into Cloud SQL table")
            app.logger.info(f"Document {path} uploaded succesfully to Cloud SQL")
            return {"status": True,
                    "response": "Document uploaded succesfully to Cloud SQL"}
        else:
            app.logger.info(f"Document {path} already exists in Cloud SQL")
            return {"status": True,
                    "response": "Document already exists in Cloud SQL"}
    
    except Exception as error:
        app.logger.error(f"Document url: {path}\n{type(error).__name__}: {error}")
        return {"status": False,
                "error": f"{type(error).__name__}: {error}"}