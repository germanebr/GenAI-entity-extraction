# CHILD Gemini API
This API allows for entity extraction from PDF documents stored in Cloud Storage using the Gemini LLM model.

## Routes
### */api/health* (GET)
Tests the API functionality.

**Response:**
```
{
  "message": "connected successfully"
}
```

### */run_pubmed* (POST)
Performs analysis of PubMed documents and stores extracted entities in the corresponding Cloud SQL table.

**Request Body:**
```
{
  "pubmed_uuid": "string",
  "pubmed_docId": "string",
  "path": "gs://<bucket_name>/<document_path>"
}
```

**Parameters:**

*pubmed_uuid*: The Pubmed UUID of the document.
*pubmed_docId*: The Pubmed docId of the document.
*path*: The Cloud Storage gs URI where the document is stored.

**Success Responses:**
Document already exists:
```
{
  "status": True,
  "response": "Document already exists in Cloud SQL"
}
```

Document uploaded successfully:
```
{
  "status": True,
  "response": "Document uploaded succesfully to Cloud SQL"
}
```

**Error Response:**
```
{
  "status": False,
  "error": "Error message"
}
```