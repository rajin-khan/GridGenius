<div align="center">

![GridGenius Banner](./documentation/GridGenius.png)

## GridGenius - AI-Powered Energy Optimization
---

### 🚀 **Project Overview**

#### **Project Title:**
**GridGenius – AI-Powered Energy Optimization**  
*Energy Demand Forecasting Using Machine Learning*

#### **Brief Summary:**
- Develop a machine learning model for forecasting urban energy demand using custom-extracted data.
- Optimize energy supply, minimize wastage, and enhance operational efficiency.
- Deploy the forecasting model via a web interface with an integrated LLM for intelligent insights.

#### **Problem Statement:**
- Inefficient energy management leads to wastage and higher costs.
- The inability to accurately predict demand causes supply-demand mismatches.
- The need for a scalable and interpretable ML-based forecasting solution.

#### **Expected Outcome:**
- Accurate energy demand predictions to aid utility providers.
- Reduction in operational costs and carbon footprint.
- A web-based platform providing actionable insights with an LLM-powered interface.

---

### 📊 **Dataset Details**

#### **Source:**
- **Custom dataset extracted from:** [BPDB Website](https://bpdb.gov.bd/)

#### **Estimated Features:**
| Feature                   | Description                                       |
|---------------------------|---------------------------------------------------|
| Date                      | Daily record date                                 |
| Day Probable Peak         | Predicted peak generation for the day             |
| Evening Probable Peak     | Predicted peak generation for the evening         |
| Actual Demand             | Real energy consumption for the day               |
| Environmental Factors     | Temperature, Humidity, Weather Conditions         |

#### **Data Collection Process:**
1. Automate extraction of daily reports using web scraping.
2. Preprocess data to remove inconsistencies.
3. Store structured data for model training.

---

### ⚙️ **Complete ML Pipeline**

1. **Data Collection:** Web scraping and processing from BPDB.
2. **Data Preprocessing:**
   Handling missing values.
   Feature engineering (time-based trends, weather impact).
3. **Exploratory Data Analysis (EDA):**
   Visualization of seasonal trends.
   Correlation analysis.
4. **Model Selection and Training:**
   Evaluate traditional and advanced ML models.
5. **Model Evaluation:**
   Metrics: RMSE, MAPE, MAE.
6. **Deployment:**
   Web application for forecasting and visualization.
   Integration with LLM for analytical insights.

---

### 🔍 **Problem Type Definition**

**Category:** Time Series Forecasting  
**Goal:** Predict future energy demand based on historical consumption and environmental factors.  
**Evaluation Metrics:**
- Root Mean Square Error (RMSE)
- Mean Absolute Percentage Error (MAPE)
- Mean Absolute Error (MAE)

---

### 🏗️ **High-Level Software Architecture**

- **Data Collection Layer:** Scraper to extract reports from BPDB.
- **Processing Layer:** Preprocessing, feature extraction.
- **Model Layer:** ML models (LSTM, ARIMA, XGBoost, etc.).
- **Web Interface Layer:** Flask/Django backend with a React frontend.
- **LLM Integration:** Assist users with querying and insights.

---

### 🛠️ **Technology Stack**

| Component                  | Technology Choices                           |
|----------------------------|----------------------------------------------|
| Data Collection            | Python (BeautifulSoup, Requests)             |
| Data Processing            | Pandas, NumPy                                |
| Model Training             | Scikit-learn, TensorFlow, XGBoost            |
| Web Framework              | Flask / Django                               |
| Frontend                   | React.js                                     |
| Database                   | PostgreSQL / SQLite                          |
| Deployment                 | AWS/GCP/Azure, Docker, CI/CD pipelines       |

---

### 🌟 **Proposed Novelty**

1. **Real-Time Prediction & Visualization:** Interactive web dashboard with live updates.
2. **LLM-Powered Insights:** Users can interact with an AI assistant to query predictions and trends.
3. **Scalability:** The model can be extended to other cities with minimal adaptation.

---

### 📚 **References**

1. **"Energy Demand Forecasting Using Machine Learning Perspective Bangladesh"**  
   - Avijit Paul Piyal et al., DOI: 10.1109/GlobConHT56829.2023.10087679

2. **"Short-Term Electrical Load Prediction for Future Generation Using Hybrid Deep Learning Model"**  
   - S. M. Anowarul Haque Sonet et al., DOI: 10.1109/ICAEEE54957.2022.9836359

---

### **👥 The Team:**
This project will be developed by:

| Name                      | Institution             | ID | GitHub | Followers |
|---------------------------|-------------------------|--  |--------|------|
| **Rajin Khan**            | North South University | 2212708042 | [![Rajin's GitHub](https://img.shields.io/badge/-rajin--khan-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rajin-khan) | ![Followers](https://img.shields.io/github/followers/rajin-khan?label=Follow&style=social) |
| **Aurongojeb Lishad**    | North South University | 2212457042 | [![Aurongojeb's GitHub](https://img.shields.io/badge/-Lishad--02-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Lishad-02) | ![Followers](https://img.shields.io/github/followers/Kabbya04?label=Follow&style=social) |
| **Pranoy Saha**    | North South University | 2131183642 | [![Pranoy's GitHub](https://img.shields.io/badge/-Pranoy28-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Pranoy28) | ![Followers](https://img.shields.io/github/followers/Pranoy28?label=Follow&style=social) |
| **Sadia Islam Mou**    | North South University | 2131724642 | [![Sadia's GitHub](https://img.shields.io/badge/-Sadiaa55-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Sadiaa55) | ![Followers](https://img.shields.io/github/followers/Sadiaa55?label=Follow&style=social) |

---

Star the repo if you wanna support more projects like this!

</div>
