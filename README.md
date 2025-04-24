<div align="center">

![GridGenius Banner](./documentation/GridGenius.png)

# ⚡ GridGenius  
### *AI-Powered Energy Forecasting & Optimization for Bangladesh*

[![Frontend - Vercel](https://img.shields.io/badge/Frontend-Vercel-brightgreen?style=for-the-badge&logo=vercel)](YOUR_VERCEL_FRONTEND_URL)
[![Backend - Railway](https://img.shields.io/badge/Backend-Railway-blue?style=for-the-badge&logo=railway)](YOUR_RAILWAY_BACKEND_URL)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

### *Website: [Live Now](grid-genius-project.vercel.app)*

---

## ✨ About the Project

**GridGenius** addresses a pressing challenge in Bangladesh’s energy sector: balancing energy generation with fluctuating national demand. We leverage machine learning and LLM-powered chat to build a smart, insightful energy planning platform.

- 📈 **Forecasts daily electricity demand** using BPDB data and advanced ML models.
- 🧠 **Chat with Ask Genius**, an explainable AI bot that answers energy-related queries based on project docs.
- 📊 **Explore trends & insights** with rich, interactive data visualizations.
- ⚡ **Optimize generation** using our "Ideal Generation" benchmark for smarter energy decisions.

---

## 💡 Why GridGenius?

🔌 **Power crises and load shedding** have long plagued Bangladesh.  
📉 **Poor demand estimation** leads to wasted resources or unmet supply.  
✅ **GridGenius bridges this gap** through AI-based forecasting and real-time interaction.

---

## 🧠 Core Highlights

- **GridOracle:** ML-based demand forecasting trained on 1800+ daily BPDB reports.
- **Ask Genius Chatbot:** Powered by Groq Llama 3 + RAG with HuggingFace embeddings.
- **Smart Insights:** Understand seasonal gaps, inefficiencies, and patterns.
- **Interactive Dashboard:** Built with Tailwind CSS, Vanilla JS, and beautiful data viz.

---

## 📊 Dataset at a Glance

| Feature            | Description                          |
|-------------------|--------------------------------------|
| `Date`            | Record date                          |
| `Demand (MW)`     | Max energy demanded                  |
| `Generation (MW)` | Max energy generated                 |
| `Temp (°C)`       | Daily avg. temperature               |
| `Season`          | Derived: high or low temp periods    |
| `IsHoliday`       | Binary: holiday or not               |
| `DemandGenGap`    | Difference between demand & supply   |

> 🔍 *Derived from 1800+ PDFs from the Bangladesh Power Development Board (BPDB)*

---

## 👥 The Team:  
This project was developed by the **'Human Forgetting'** Team at **North South University**:

| Name                  | Institution             | ID         | GitHub                                                                                      | Followers                                                   |
|-----------------------|-------------------------|------------|---------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| **Rajin Khan**        | North South University  | 2212708042 | [![Rajin's GitHub](https://img.shields.io/badge/-rajin--khan-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rajin-khan)         | ![Followers](https://img.shields.io/github/followers/rajin-khan?label=Follow&style=social) |
| **Aurongojeb Lishad** | North South University  | 2212457042 | [![Aurongojeb's GitHub](https://img.shields.io/badge/-Lishad--02-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Lishad-02)       | ![Followers](https://img.shields.io/github/followers/Kabbya04?label=Follow&style=social)     |
| **Pranoy Saha**       | North South University  | 2131183642 | [![Pranoy's GitHub](https://img.shields.io/badge/-Pranoy28-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Pranoy28)             | ![Followers](https://img.shields.io/github/followers/Pranoy28?label=Follow&style=social)     |
| **Sadia Islam Mou**   | North South University  | 2131724642 | [![Sadia's GitHub](https://img.shields.io/badge/-Sadiaa55-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Sadiaa55)             | ![Followers](https://img.shields.io/github/followers/Sadiaa55?label=Follow&style=social)     |

---

## 🙌 Acknowledgements

- 📊 Data: Bangladesh Power Development Board  
- 🤖 LLM: Groq API, Hugging Face Inference API  
- 🧠 Vector Search: ChromaDB  
- ⚙️ Backend: FastAPI  
- 🎨 UI: Tailwind CSS  

---

⭐ If you found this project inspiring, star the repo and support more energy-conscious innovations!  

</div>
