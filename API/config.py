import os

class Config:
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'gcp-service-account.json')

    GEMINI_MODEL = "gemini-1.5-pro-001"
    GEMINI_TEMPERATURE = 0
    GEMINI_MAX_TOKENS = 8192
    GEMINI_TOP_P = 0.95
    GEMINI_LLM_RETRIES = 3

    CLOUD_SQL_INSERT = os.getenv('CLOUD_SQL_INSERT', 'url-for-inserting-into-cloud-sql-database')
    CLOUD_SQL_RETRIEVE = os.getenv('CLOUD_SQL_RETRIEVE', 'url-for-retrieving-data-from-cloud-sql-database')
    CLOUD_SQL_INSERT_TABLE = "cloud-sql-table"
    CLOUD_SQL_DATABASE = "cloud-sql-database"
    CLOUD_SQL_GET_DOI_EXISTENCE_QUERY = "PUBMED_GET_DOI_EXISTENCE" # This query is stored on the microservice and checks if the document is already stored in cloud sql
    # SELECT EXISTS(SELECT * from cloud-sql-database.cloud-sql-table WHERE DOI = %s);