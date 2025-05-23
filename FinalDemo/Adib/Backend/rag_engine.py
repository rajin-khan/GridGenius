import os
import glob
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from groq import Groq
from utils import extract_text_from_file
from typing import List, Dict, AsyncGenerator
import asyncio # Import asyncio

# --- Initialization ---

os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq Client
groq_client = Groq(api_key=GROQ_API_KEY)

# Chroma Client
chroma_client = PersistentClient(path="./chroma_storage")
collection = chroma_client.get_or_create_collection(name="rag_collection")

# Embedder
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# --- Prewarm the embedder ---
# This ensures model and tokenizer are loaded BEFORE first real query
print("Pre-warming embedder...")
embedder.encode(["GridGenius startup warmup."])
print("Embedder ready.")

# --- Core Functions ---

def load_all_documents(folder_path="./documents"):
    """
    Loads and embeds all documents from a given folder into ChromaDB.
    """
    file_paths = glob.glob(folder_path + "/*")
    documents = []
    doc_ids = []

    for i, file_path in enumerate(file_paths):
        text = extract_text_from_file(file_path)
        if text:
            documents.append(text)
            doc_ids.append(f"doc_{i}")

    if documents:
        embeddings = embedder.encode(documents).tolist()
        collection.add(documents=documents, embeddings=embeddings, ids=doc_ids)
    return len(documents)

async def query_rag(chat_history: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """
    Given the full chat history, retrieves top documents and streams a response using Groq LLM.
    Yields response chunks as strings.
    """
    if not chat_history:
        yield "Error: Chat history is empty."
        return

    user_query = chat_history[-1]['content']  # Last user input

    try:
        query_embedding = embedder.encode([user_query]).tolist()

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=1,
            include=["documents"]
        )

        retrieved_docs = results.get('documents', [[]])[0] # Handle case where no documents are found
        combined_context = "\n\n".join(retrieved_docs) if retrieved_docs else "No relevant context found."

        # GridGenius system prompt
        # Inside query_rag function in rag_engine.py

        # GridGenius system prompt (Revised for Natural Tone & Tables)
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

        # Build full messages array
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Here is the relevant context retrieved from documents:\n\n{combined_context}"}
        ] + chat_history

        # Use streaming - create() call itself is synchronous when stream=True
        stream = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            stream=True
        )

        # Iterate SYNCHRONOUSLY over the stream within the ASYNC function
        for chunk in stream: # Changed back from 'async for'
            # Check if delta and content exist before accessing
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                 content = chunk.choices[0].delta.content
                 yield content # Yield the actual content string
                 # Add a small await to allow event loop to process other tasks if needed
                 # This helps prevent blocking if the stream processing takes time
                 await asyncio.sleep(0.001)


    except Exception as e:
        print(f"Error during RAG query or streaming: {e}")
        # Optionally yield a user-facing error message
        yield f"⚠️ An error occurred while processing the request: {str(e)}"