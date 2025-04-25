# Backend/api.py

from fastapi import APIRouter, UploadFile, File, HTTPException # Add HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from pydantic import BaseModel
from rag_engine import load_all_documents, query_rag, collection # Import collection
import os
import joblib # Import joblib
import numpy as np # Import numpy
import asyncio # Keep asyncio if needed elsewhere

# --- New: Load Model and Scaler on Startup ---
MODEL_PATH = "energy_model.pkl"
SCALER_PATH = "scaler.pkl"
MODEL = None
SCALER = None

try:
    if os.path.exists(MODEL_PATH):
        MODEL = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    else:
        print(f"Error: Model file not found at {MODEL_PATH}")

    if os.path.exists(SCALER_PATH):
        SCALER = joblib.load(SCALER_PATH)
        print(f"Scaler loaded successfully from {SCALER_PATH}")
    else:
        print(f"Error: Scaler file not found at {SCALER_PATH}")

except Exception as e:
    print(f"Error loading model or scaler: {e}")
    # Depending on criticality, you might want to raise an exception here
    # raise RuntimeError(f"Could not load model/scaler: {e}") from e

# --- End New Model Loading ---


router = APIRouter()

os.makedirs("./documents", exist_ok=True)

class QueryRequest(BaseModel):
    chat_history: List[dict]  # Each message is a dict with 'role' and 'content'

# --- New: Pydantic Model for Prediction Input ---
class PredictionRequest(BaseModel):
    temp: float
    year: int
    month: int
    season: int # Expecting 0 or 1
    isholiday: int # Expecting 0 or 1
    day: int
# --- End New Pydantic Model ---

@router.post("/upload/")
async def upload_documents(files: List[UploadFile] = File(...)):
    # (Keep existing upload logic as is)
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
    response_generator = query_rag(request.chat_history)
    return StreamingResponse(response_generator, media_type="text/plain")


# --- New: Prediction Endpoint ---
@router.post("/predict/")
async def predict_demand(request: PredictionRequest):
    """
    Predicts energy demand based on input features.
    """
    if MODEL is None or SCALER is None:
        raise HTTPException(status_code=503, detail="Model or Scaler not loaded. Service unavailable.")

    try:
        # Extract data from request
        temp_raw = request.temp
        year = request.year
        month = request.month
        season = request.season
        isholiday = request.isholiday
        day = request.day

        # --- Scaling Logic (copied and adapted from predict_energy_demand.py) ---
        # IMPORTANT: Verify these indices (2 and 0) match your scaler's features!
        # Index 2 is assumed to be 'Temp(C)' based on the original script
        # Index 0 is assumed to be 'Demand(MW)' based on the original script
        if len(SCALER.data_min_) <= 2 or len(SCALER.data_range_) <= 2:
             raise ValueError("Scaler does not have enough features for temperature scaling (index 2).")
        temp_min = SCALER.data_min_[2]
        temp_range = SCALER.data_range_[2]
        if temp_range == 0: # Avoid division by zero
            raise ValueError("Scaler range for temperature (index 2) is zero.")
        temp_scaled = (temp_raw - temp_min) / temp_range

        # Create input array in the specific order expected by the model
        # Order: temp_scaled, year, month, season, isholiday, day
        X_input = np.array([[temp_scaled, year, month, season, isholiday, day]])
        # --- End Scaling Logic ---

        # --- Prediction ---
        scaled_prediction = MODEL.predict(X_input)
        # --- End Prediction ---

        # --- Inverse Scaling Logic ---
        if len(SCALER.data_min_) == 0 or len(SCALER.data_range_) == 0:
             raise ValueError("Scaler does not have enough features for demand inverse scaling (index 0).")
        demand_min = SCALER.data_min_[0]
        demand_range = SCALER.data_range_[0]
        if demand_range == 0: # Avoid division by zero
            raise ValueError("Scaler range for demand (index 0) is zero.")
        predicted_demand = scaled_prediction[0] * demand_range + demand_min
        # --- End Inverse Scaling Logic ---

        return {"predicted_demand": predicted_demand}

    except ValueError as ve:
        print(f"Data processing error: {ve}")
        raise HTTPException(status_code=400, detail=f"Invalid input or scaler configuration: {ve}")
    except Exception as e:
        print(f"Prediction error: {e}")
        # Log the full error details for debugging
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An internal error occurred during prediction: {e}")

# --- End New Prediction Endpoint ---


# --- Document Loading on Startup (Keep as is) ---
try:
    print("Loading documents on startup...")
    try:
        count_before = collection.count()
        print(f"Documents in DB before load: {count_before}")
    except Exception:
         print("Collection not found or empty before load.")
         count_before = 0

    num_loaded = load_all_documents()
    count_after = collection.count()
    print(f"Loaded {num_loaded} new files.")
    print(f"Total documents in DB after load: {count_after}")
except Exception as e:
    print(f"Error loading documents on startup: {e}")
# --- End Document Loading ---