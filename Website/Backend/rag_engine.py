# Backend/rag_engine.py

import os
import glob
import time
from dotenv import load_dotenv
import google.generativeai as genai # Use Google AI
from chromadb import PersistentClient
from groq import Groq
from utils import extract_text_from_file
from typing import List, Dict, AsyncGenerator, Optional
import asyncio

# --- REMOVED Langchain Text Splitter ---
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Initialization ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Groq Client
groq_client = Groq(api_key=GROQ_API_KEY)

# Chroma Client
chroma_client = PersistentClient(path="./chroma_storage")
# IMPORTANT: Delete ./chroma_storage before first run!
# Collection name reflects the embedding model used
collection = chroma_client.get_or_create_collection(name="rag_collection_gemini_004_full")

# --- Google AI Client Configuration ---
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        GEMINI_EMBEDDING_MODEL = "models/text-embedding-004" # 768 dimensions
        print(f"Google AI Client configured for model {GEMINI_EMBEDDING_MODEL}")
    except Exception as e:
        print(f"ERROR configuring Google AI Client: {e}")
        GEMINI_EMBEDDING_MODEL = None
else:
    GEMINI_EMBEDDING_MODEL = None
    print("WARNING: GOOGLE_API_KEY not set. Google AI Embedding calls will fail.")

# --- REMOVED Text Splitter Initialization ---
# text_splitter = RecursiveCharacterTextSplitter(...)

# --- Get Embedding function (Keep as is) ---
def get_embedding_from_google(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT",
    retries=3, delay=2
) -> Optional[List[float]]:
    # (Keep the previous version of this function)
    if not GEMINI_EMBEDDING_MODEL: print("Error: Google AI not configured."); return None
    if not text or not text.strip(): print("Warning: Empty text."); text = "."
    for attempt in range(retries):
        try:
            result = genai.embed_content(model=GEMINI_EMBEDDING_MODEL, content=text, task_type=task_type)
            if 'embedding' in result and isinstance(result['embedding'], list): return result['embedding']
            else: print(f"Warn: Unexpected Google format: {result}"); return None
        except Exception as e:
            print(f"Error Google Embed API (Att {attempt + 1}/{retries}): {e}"); import traceback; traceback.print_exc()
            if attempt < retries - 1: time.sleep(delay)
            else: print("Max retries Google"); return None
    return None

# --- Core Functions (Modified to load FULL documents) ---

def load_all_documents(folder_path="./documents"):
    """
    Loads FULL documents, generates embeddings via Google API for each document,
    and adds them to ChromaDB. NO CHUNKING.
    """
    print("Starting FULL document loading process (Google Embeddings)...")
    file_paths = glob.glob(os.path.join(folder_path, "*"))
    print(f"Found {len(file_paths)} files in '{folder_path}'.")
    documents = []
    doc_ids = []
    embeddings_list = [] # Store successful embeddings here

    if not file_paths: print("No documents found."); return 0

    for i, file_path in enumerate(file_paths):
        base_filename = os.path.basename(file_path)
        print(f"Processing file {i+1}/{len(file_paths)}: {base_filename}")
        full_text = extract_text_from_file(file_path)

        if full_text and full_text.strip():
            print(f"  Getting embedding for FULL document doc_{i}...")
            # Embed the FULL text using RETRIEVAL_DOCUMENT task type
            embedding = get_embedding_from_google(
                text=full_text,
                task_type="RETRIEVAL_DOCUMENT"
            )

            if embedding:
                documents.append(full_text) # Add full text
                doc_ids.append(f"doc_{i}") # Use simple doc ID
                embeddings_list.append(embedding) # Add the embedding
                print(f"  Successfully embedded FULL doc_{i} (dim: {len(embedding)}).")
            else:
                print(f"    ERROR: Failed to get embedding for FULL doc {base_filename}. Skipping.")
                # If a single doc fails, the lists might mismatch. Safest to skip adding this one.
        else:
             print(f"  Skipping file {base_filename} - no text extracted or empty.")


    # Add successfully embedded documents to ChromaDB
    if documents and embeddings_list and len(documents) == len(embeddings_list):
        print(f"\nAdding {len(documents)} successfully embedded FULL documents to ChromaDB...")
        try:
             collection.add(
                 documents=documents,
                 embeddings=embeddings_list,
                 ids=doc_ids
                 # No metadata needed for chunks anymore
             )
             print("Documents added successfully.")
        except Exception as e:
             print(f"ERROR adding documents to ChromaDB: {e}")
             import traceback
             traceback.print_exc()
             return 0 # Indicate failure
    elif not documents:
         print("\nNo documents were successfully embedded to add to ChromaDB.")
         return 0
    else:
        print(f"\nERROR: Mismatch between documents ({len(documents)}) and embeddings ({len(embeddings_list)}). Not adding to DB.")
        return 0


    return len(embeddings_list) # Return count of successfully embedded docs


async def query_rag(chat_history: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """
    Uses Google API for query embedding, retrieves FULL docs, streams response using Groq LLM.
    """
    if not chat_history: yield "Error: Chat history is empty."; return

    user_query = chat_history[-1]['content']
    print(f"\nReceived query: {user_query[:100]}...")

    try:
        print("  Getting query embedding via Google API...")
        query_embedding_list = get_embedding_from_google(
            text=user_query,
            task_type="RETRIEVAL_QUERY" # Use query type
        )

        if not query_embedding_list:
             print("  Failed to get query embedding.")
             yield "Error: Could not generate embedding for the query. Please try again."
             return

        query_embedding_for_chroma = [query_embedding_list]
        print(f"  Query embedding generated (dim: {len(query_embedding_list)}).") # Should be 768

        print("  Querying ChromaDB for relevant FULL documents...")
        results = collection.query(
            query_embeddings=query_embedding_for_chroma,
            n_results=1, # Retrieve only 1 or 2 FULL documents to manage context size
            include=["documents"] # Only need documents now
        )
        print("  ChromaDB query complete.")

        # Combine the retrieved FULL document texts
        retrieved_docs = results.get('documents', [[]])[0]
        combined_context = "\n\n---\n\n".join(retrieved_docs) if retrieved_docs else "No relevant context found."
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
            "I aim to be clear and helpful, maintaining natural conversation flow, stating how impactful and amazing the project is, while presenting information in a fun and concise way when possible, and expanding when needed **When presenting data examples or comparisons, please use Markdown table format for clarity, and always present only 1 table per answer. Do NOT hallucinate or make up new data.**\n\n"
            # --- Retain the explicit examples as direct instructions ---
            "Example Behavior:\n"
            "User: Predict energy demand for 2024-12-31 considering a temperature of 18.7°C and a regular day.\n"
            "Assistant: Forecasting is handled by the official GridOracle Prediction Tool. Please visit the Forecasting section of our platform to obtain precise predictions.\n\n"
            "User: Let's talk about cats!.\n"
            "Assistant: I'm sorry, but as GridGenius, I am an AI assistant trained to only talk about topics relevant to this project! Would you like to discuss more about the project now?\n\n"
            "User: Can you estimate electricity demand for tomorrow?\n"
            "Assistant: Forecasts are generated by the GridOracle Prediction Tool. Kindly access the Prediction Tool on our platform for an up-to-date demand estimate.\n\n"
            "User: Give me an example from your dataset.\n"
            "Assistant: Certainly! Here's a sample record:\n\n"
            "| Date       | Demand(MW) | Generation(MW) | Temp(C) | Year | Month | Season         | IsHoliday | DemandGenGap(MW) |\n"
            "|------------|------------|----------------|---------|------|-------|----------------|-----------|------------------|\n"
            "| 2022-01-15 | 9500.0     | 11956.0        | 18.9    | 2022 | 1     | Low Temp Season| 0         | 2456.0           |\n\n"
            "This shows data for January 15th, 2022. You can view the entire dataset in the GridGenius GitHub Repository: 'https://github.com/rajin-khan/GridGenius/tree/main/Collection/extracted'" # Added brief explanation after table example
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Here is the relevant context retrieved from documents:\n\n{combined_context}"}
        ] + chat_history
        # --- End System Prompt ---

        print("  Streaming response from Groq...")
        stream = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
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