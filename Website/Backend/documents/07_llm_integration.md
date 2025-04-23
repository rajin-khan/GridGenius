# GridGenius: LLM Integration and RAG

**Purpose of the LLM:**
*   Act as an **explainable AI** component for the GridGenius project.
*   **Bridge the gap** between energy experts and regular users.
*   Explain project details:
    *   How the forecasting model works.
    *   Information about the dataset used.
    *   The overall project goals and methodology.
*   Function as an interactive **chatbot**.

**Implementation Method:**
*   The primary method planned is **fine-tuning**, specifically using **LoRA (Low Rank Adaptation)**.

**LoRA (Low Rank Adaptation):**
*   Based on Edward Hu's 2021 paper.
*   An efficient fine-tuning technique for large language models (LLMs).
*   **How it works:**
    *   The **majority** of the pre-trained LLM's weights are **frozen** (not changed). This retains the model's core fluency, knowledge, and abilities.
    *   **Small, trainable "adapter" matrices** (LoRA adapters) with low rank are injected into specific layers of the model (often the Transformer layers).
    *   Only these **small adapters (a few million parameters)** are trained/fine-tuned on the specific dataset (in this case, text describing the GridGenius project).
*   **Benefits:**
    *   **Computationally cheaper:** Requires significantly less computing power and memory compared to full fine-tuning.
    *   **Faster training:** Training only the adapters is much faster.
    *   **Preserves base model:** Retains most of the original LLM's capabilities.
    *   **Specialization:** Allows the model to specialize in the specific information it's fine-tuned on (GridGenius project details).

**Current Implementation (RAG):**
*   While LoRA fine-tuning might be a future goal, the *current* chatbot implementation uses **RAG (Retrieval-Augmented Generation)**.
*   RAG works by:
    1.  Storing project information (like these markdown files) in a vector database (ChromaDB).
    2.  When a user asks a question, the system retrieves the most relevant text snippets from the database.
    3.  These snippets are provided as context to the LLM (Groq Llama 3) along with the user's query and chat history.
    4.  The LLM generates an answer based on the provided context and conversation.