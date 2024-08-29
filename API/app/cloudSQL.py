import requests
import json

from config import Config

class CloudSQL():
    def insertWithParameters(params):
        headers = {'Content-Type': 'application/json'}
        todo = {'table': Config.CLOUD_SQL_INSERT_TABLE,
                'database': Config.CLOUD_SQL_DATABASE,
                'data': [params]}

        response = requests.post(Config.CLOUD_SQL_INSERT,
                                 json = todo,
                                 headers = headers)
        
        response = response.json()
        # print(response)
        
        if not response["status"]:
            raise Exception(response['res'][0]['message'])
    
    def get_existence(params):
        headers = {'Content-Type': 'application/json'}
        todo = {'queryName': Config.CLOUD_SQL_GET_DOI_EXISTENCE_QUERY,
                'database': Config.CLOUD_SQL_DATABASE,
                'parameters': params}

        response = requests.post(Config.CLOUD_SQL_RETRIEVE,
                                 json = todo,
                                 headers = headers)
        
        # print(type(response.json()))
        # print(response.json())
        response = json.loads(response.json()['res'])
        exists = list(response['data'][0].values())[0]
        return exists