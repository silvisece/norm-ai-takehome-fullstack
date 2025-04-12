"""
Please create an endpoint that accepts a query string, e.g., "what happens if I steal 
from the Sept?" and returns a JSON response serialized from the Pydantic Output class.
"""
import yaml
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from llama_index.core.schema import Document
from app.qdrant_service import QdrantService, Output
from app.process_text import DocumentService

with open("app/config.yml", 'r') as file:
    config = yaml.safe_load(file)

app = FastAPI()
qdrant_service = QdrantService(k=config['k'])

@app.on_event("startup")
def startup_event():
    docs = DocumentService.read_docs_from_json(config['processed_file_path'])
    qdrant_service.connect()
    qdrant_service.load(docs)

@app.get("/query", response_model=Output)
def query_endpoint(query: str = Query(..., min_length=1, max_length=1000)):
    try:
        result = qdrant_service.query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
