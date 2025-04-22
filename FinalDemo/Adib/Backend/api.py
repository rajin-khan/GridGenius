from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
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
    num_loaded_total = 0
    errors = []
    for uploaded_file in files:
        try:
            contents = await uploaded_file.read()
            file_path = f"./documents/{uploaded_file.filename}"
            with open(file_path, "wb") as f:
                f.write(contents)
            print(f"Saved file: {uploaded_file.filename}")
        except Exception as e:
            errors.append(f"Failed to save {uploaded_file.filename}: {e}")
            print(f"Error saving file {uploaded_file.filename}: {e}")

    if errors:
         # Still attempt loading even if some saves failed
        print("Attempting to load documents despite save errors...")

    try:
        num_loaded = load_all_documents()
        num_loaded_total += num_loaded
        print(f"Loaded {num_loaded} documents in this batch.")
    except Exception as e:
        errors.append(f"Failed to load documents into ChromaDB: {e}")
        print(f"Error loading documents: {e}")


    if errors:
        return {"message": f"Processed uploads with errors. Successfully loaded {num_loaded_total} documents.", "errors": errors}
    else:
        return {"message": f"Successfully uploaded and loaded {num_loaded_total} documents into ChromaDB."}


@router.post("/query/")
async def query_document(request: QueryRequest):
    """
    Handles querying the RAG engine and returns a streaming response.
    """
    # query_rag is now an async generator
    response_generator = query_rag(request.chat_history)
    return StreamingResponse(response_generator, media_type="text/plain")

from rag_engine import load_all_documents, collection # Ensure collection is imported if needed for count
try:
    print("Loading documents on startup...")
    # Ensure collection exists before trying to count (optional check)
    try:
        count_before = collection.count()
        print(f"Documents in DB before load: {count_before}")
    except Exception: # Handle case where collection might not exist yet fully
         print("Collection not found or empty before load.")
         count_before = 0

    num_loaded = load_all_documents() # This loads from ./documents
    count_after = collection.count()
    print(f"Loaded {num_loaded} new files.")
    print(f"Total documents in DB after load: {count_after}")
except Exception as e:
    print(f"Error loading documents on startup: {e}")