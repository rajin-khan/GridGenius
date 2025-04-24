# Backend/rag_engine.py

import os
import glob
import time
from dotenv import load_dotenv
import requests # Use requests for HTTP calls
from chromadb import PersistentClient
from groq import Groq
from utils import extract_text_from_file
from typing import List, Dict, AsyncGenerator, Optional
import asyncio # Import asyncio

# --- Initialization ---

# os.environ["TOKENIZERS_PARALLELISM"] = "false" # Not needed for API

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_TOKEN = os.getenv("HF_API_TOKEN") # Load HF Token from .env

# Groq Client
groq_client = Groq(api_key=GROQ_API_KEY)

# Chroma Client
chroma_client = PersistentClient(path="./chroma_storage")
collection = chroma_client.get_or_create_collection(name="rag_collection")

# --- Hugging Face Inference API Configuration ---
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
HF_API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{MODEL_ID}"

if not HF_API_TOKEN:
    print("WARNING: HF_API_TOKEN environment variable not set. Embedding API calls will fail.")
    HF_HEADERS = {}
else:
    HF_HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}
# --- End HF Config ---

# --- REMOVED Local Embedder ---
# _embedder = None
# def get_embedder(): ...
# --- End Removed ---


# --- New Function: Get Embedding from API ---
def get_embedding_from_api(text: str, retries=3, delay=2) -> Optional[List[float]]:
    """Calls the Hugging Face Inference API to get embeddings."""
    if not HF_HEADERS.get("Authorization"):
        print("Error: HF_API_TOKEN is not configured.")
        return None
    if not text or not text.strip():
        print("Warning: Attempted to embed empty text.")
        return None # Avoid API call for empty strings

    payload = {"inputs": text, "options": {"wait_for_model": True}}

    for attempt in range(retries):
        try:
            response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=30) # Increased timeout slightly
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            result = response.json()

            # --- Response Parsing (Adjust if necessary based on model/pipeline) ---
            # For feature-extraction with sentence-transformers, usually nests embedding
            if isinstance(result, list) and result:
                if isinstance(result[0], list) and isinstance(result[0][0], float):
                    # Common case: [[embedding_vector]]
                    return result[0]
                elif isinstance(result[0], float):
                     # Case: [embedding_vector] (less common for this pipeline)
                     return result
            # Handle potential dictionary response for some models/errors
            elif isinstance(result, dict) and 'error' in result:
                 print(f"Error from HF API: {result['error']}")
                 # Optionally check for specific error types if needed
                 if attempt < retries - 1:
                      print(f"Retrying in {delay}s...")
                      time.sleep(delay)
                      continue # Go to next retry attempt
                 else:
                      return None # Max retries for API error
            
            print(f"Warning: Unexpected embedding format received: {type(result)}. Full response: {result}")
            return None # Return None if format is not recognized

        except requests.exceptions.Timeout:
            print(f"Error: Timeout calling HF Inference API (Attempt {attempt + 1}/{retries})")
            if attempt < retries - 1:
                print(f"Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print("Max retries reached for timeout.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling HF Inference API (Attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print("Max retries reached for connection error.")
                return None
        except Exception as e: # Catch other potential errors like JSON decoding
            print(f"Unexpected error processing API response (Attempt {attempt + 1}/{retries}): {e}")
            try:
                print(f"Raw Response Text: {response.text}") # Log raw text on error
            except NameError: pass # response might not be defined
            if attempt < retries - 1:
                 print(f"Retrying in {delay}s...")
                 time.sleep(delay)
            else:
                 print("Max retries reached for unexpected error.")
                 return None

    return None # Should not be reached if loop finishes, but safety return
# --- End New Function ---


# --- Core Functions (Modified) ---

def load_all_documents(folder_path="./documents"):
    """
    Loads documents, generates embeddings via API, and adds to ChromaDB.
    """
    print("Starting document loading process...")
    file_paths = glob.glob(os.path.join(folder_path, "*")) # Use os.path.join
    print(f"Found {len(file_paths)} files in '{folder_path}'.")
    documents = []
    doc_ids = []
    embeddings_list = [] # Store embeddings here

    if not file_paths:
        print("No documents found in the specified folder.")
        return 0

    for i, file_path in enumerate(file_paths):
        print(f"Processing file {i+1}/{len(file_paths)}: {os.path.basename(file_path)}")
        text = extract_text_from_file(file_path)
        if text:
            print(f"  Getting embedding for doc_{i}...")
            embedding = get_embedding_from_api(text) # <-- USE API FUNCTION
            if embedding:
                documents.append(text)
                doc_ids.append(f"doc_{i}")
                embeddings_list.append(embedding) # Append the valid embedding
                print(f"  Successfully embedded doc_{i}.")
            else:
                print(f"  Failed to get embedding for doc_{i}, skipping.")
        else:
             print(f"  Skipping file {os.path.basename(file_path)} - no text extracted.")


    if documents:
        print(f"\nAdding {len(documents)} successfully embedded documents to ChromaDB...")
        try:
             # Check counts before adding (optional)
             # count_before = collection.count()
             collection.add(documents=documents, embeddings=embeddings_list, ids=doc_ids)
             # count_after = collection.count()
             # print(f"ChromaDB count changed from {count_before} to {count_after}")
             print("Documents added successfully.")
        except Exception as e:
             print(f"ERROR adding documents to ChromaDB: {e}")
             # Potentially raise exception or handle recovery
    else:
         print("\nNo documents were successfully embedded to add to ChromaDB.")

    return len(documents) # Return count of successfully processed docs

async def query_rag(chat_history: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """
    Uses API for query embedding, retrieves docs, streams response using Groq LLM.
    """
    if not chat_history:
        yield "Error: Chat history is empty."
        return

    user_query = chat_history[-1]['content']
    print(f"\nReceived query: {user_query[:100]}...") # Log start of query processing

    try:
        print("  Getting query embedding from API...")
        query_embedding_list = get_embedding_from_api(user_query) # <-- USE API FUNCTION

        if not query_embedding_list:
             print("  Failed to get query embedding.")
             yield "Error: Could not generate embedding for the query. Please try again."
             return

        # ChromaDB expects embeddings as a list of lists for querying
        query_embedding_for_chroma = [query_embedding_list]
        print("  Query embedding generated.")

        print("  Querying ChromaDB...")
        results = collection.query(
            query_embeddings=query_embedding_for_chroma,
            n_results=1, # Still using n_results=1 as per your previous code
            include=["documents"]
        )
        print("  ChromaDB query complete.")

        retrieved_docs = results.get('documents', [[]])[0]
        combined_context = "\n\n".join(retrieved_docs) if retrieved_docs else "No relevant context found."
        print(f"  Retrieved {len(retrieved_docs)} documents for context.")

        # --- System Prompt and Message Building (Keep As Is) ---
        system_prompt = (
            "Hello! I'm GridGenius, an AI assistant from the 'Human Forgetting' team at North South University (Adib Ar Rahman Khan, Aurongojeb Lishad, Pranoy Saha, and Sadia Islam Mou). "
            "My purpose is to help explore national energy optimization for Bangladesh.\n\n"
            "I can discuss topics like:\n"
            "⚡ Electricity demand patterns and forecasting concepts\n"
            "🌦️ How climate and events (like holidays) influence energy needs\n"
            "💡 Optimizing energy generation strategies\n"
            "📊 Summarizing energy insights\n\n"
            "Think of me as focused specifically on these energy-related areas for Bangladesh. To give you the best information, I'll primarily use the relevant details found in the document snippets we're looking at during our conversation. If the context doesn't cover your question, I'll be upfront about that limitation.\n\n"
            "Accuracy is important! I stick to the facts provided and my specialized knowledge area. I won't invent data, statistics, or specific predictions. For actual, up-to-the-minute forecasts, please use the official GridGenius Prediction Tool on the platform – that system handles the real-time calculations based on our fine-tuned Transformer model.\n\n"
            "I aim to be clear and helpful. **When presenting data examples or comparisons, please use Markdown table format for clarity.**\n\n"
            # --- Retain the explicit examples as direct instructions ---
            "Example Behavior:\n"
            "User: Predict energy demand for 2024-12-31 considering a temperature of 18.7°C and a regular day.\n"
            "Assistant: Forecasting is handled by the official GridGenius Prediction Tool. Please visit the Forecasting section of our platform to obtain precise predictions.\n\n"
            "User: Can you estimate electricity demand for tomorrow?\n"
            "Assistant: Forecasts are generated by the GridGenius Prediction System. Kindly access the Prediction Tool on our platform for an up-to-date demand estimate.\n\n"
            "User: Give me an example from your dataset.\n"
            "Assistant: Certainly! Here's a sample record:\n\n"
            "| Date       | Demand(MW) | Generation(MW) | Temp(C) | Year | Month | Season         | IsHoliday | DemandGenGap(MW) |\n"
            "|------------|------------|----------------|---------|------|-------|----------------|-----------|------------------|\n"
            "| 2022-01-15 | 9500.0     | 11956.0        | 18.9    | 2022 | 1     | Low Temp Season| 0         | 2456.0           |\n\n"
            "This shows data for January 15th, 2022." # Added brief explanation after table example
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Here is the relevant context retrieved from documents:\n\n{combined_context}"}
        ] + chat_history
        # --- End System Prompt ---

        print("  Streaming response from Groq...")
        stream = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            stream=True
        )

        # Keep your original loop structure as it worked for you
        content_streamed = False
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                 content = chunk.choices[0].delta.content
                 yield content
                 content_streamed = True
                 await asyncio.sleep(0.001) # Keep sleep if it helped responsiveness

        if not content_streamed:
            print("  Warning: Groq stream finished without yielding content.")
            # yield "..." # Optionally yield a default message if nothing came back

        print("  Groq stream finished.")

    except Exception as e:
        print(f"Error during RAG query or streaming: {e}")
        import traceback
        traceback.print_exc() # Print full traceback for debugging
        yield f"⚠️ An error occurred while processing the request: {str(e)}" 