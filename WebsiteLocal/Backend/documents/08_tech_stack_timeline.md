# GridGenius: Tech Stack and Project Timeline

**Tech Stack:**
The project utilizes the following technologies across different layers:

*   **Data Collection:** Python (Libraries: BeautifulSoup, Requests)
*   **Data Processing:** Python (Libraries: pandas, NumPy)
*   **Model Training:** Python (Libraries: Scikit-Learn, TensorFlow (potentially for Transformer/LSTM), XGBoost)
*   **Web Framework (Backend):** Python (FastAPI - current implementation uses this, Flask/Django also considered)
*   **Frontend:** HTML, CSS (Tailwind CSS), JavaScript (Vanilla JS currently) (React considered)
*   **Database (Vector DB for RAG):** ChromaDB (current) (SQLite mentioned, likely for other potential structured data)
*   **LLM Provider (for RAG):** Groq
*   **Deployment:** Considerations include AWS/Azure, Docker, CI/CD pipelines.

**Project Timeline Overview (Approx. 10 Weeks):**

*   **Phase 1: Dealing with Data (Weeks 1-2)**
    *   Week 1: Data Collection (Web Scraping Automation), Preprocessing (Cleaning).
    *   Week 2: Exploratory Data Analysis (EDA), Statistical Analysis, Visualization, Correlation Identification.
*   **Phase 2: Managing the Model (Weeks 3-7)**
    *   Weeks 3-4: Model Development & Training (Baseline models, Advanced models like Transformer/LSTM).
    *   Week 5: Model Evaluation & Optimization (Hyperparameter tuning, Cross-validation, Metric comparison).
    *   Weeks 6-7: Model Deployment (Prepare model artifacts, Build API endpoint - e.g., Flask/FastAPI, Test API).
*   **Phase 3: Cementing the Services (Weeks 8-10)**
    *   Weeks 8-9: Web App Development (Backend integration with API, Frontend UI development).
    *   Week 10: System Testing, Documentation (Project report/paper), Final Presentation preparation.
*   **Phase 4: Preparing the Paper (Ongoing throughout)**
    *   Literature Review
    *   Defining Objectives, Methodology
    *   Writing Introduction, Problem Statement
    *   Detailing Methodology, Implementation
    *   Presenting Results & Discussion
    *   Writing Conclusion, Abstract
    *   Preparing Figures, Tables, Citations
    *   Final Proofreading & Formatting (e.g., for IEEE).