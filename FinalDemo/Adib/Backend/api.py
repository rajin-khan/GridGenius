from fastapi import APIRouter, UploadFile, File
from typing import List
from pydantic import BaseModel
from rag_engine import load_all_documents, query_rag
import os

router = APIRouter()

os.makedirs("./documents", exist_ok=True)

class QueryRequest(BaseModel):
    chat_history: List[dict]  # Each message is a dict with 'role' and 'content'

@router.post("/upload/")
async def upload_documents(files: List[UploadFile] = File(...)):
    for uploaded_file in files:
        contents = await uploaded_file.read()
        file_path = f"./documents/{uploaded_file.filename}"
        with open(file_path, "wb") as f:
            f.write(contents)

    num_loaded = load_all_documents()
    return {"message": f"Successfully loaded {num_loaded} documents into ChromaDB."}

@router.post("/query/")
async def query_document(request: QueryRequest):
    answer = query_rag(request.chat_history)
    return {"answer": answer}