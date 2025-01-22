# Topic Proposal
---

## 📝 **Topic Name**:
# 🔍 Predicting Bangladesh's Inflation Trend: Key Insights and Future Outlook📊

## Description
This project aims to forecast inflation trends and predict future inflation rates in Bangladesh using advanced machine learning techniques, with a focus on deep learning models.
Inflation is a critical economic indicator that affects policy decisions, businesses, and individual livelihoods.
Accurate forecasting of inflation rates can assist policymakers and stakeholders in planning and implementing effective economic strategies. 
This project leverages historical economic data and applies machine learning models to capture patterns, trends, and relationships in inflation-related factors.

## Existing Papers 
Below are some relevant research papers on inflation forecasting using machine learning and deep learning:

 ### 1. "Inflation Dynamics of Bangladesh: An Empirical Analysis"
   - Link: https://ejbmr.org/index.php/ejbmr/article/view/1958
   - Description: The paper "Inflation Dynamics of Bangladesh: An Empirical Analysis" explores the determinants of inflation in Bangladesh using annual data from 1986 to 2021.

**Key Variables:**

* Inflation (Consumer Price Index - CPI)

* Gross Domestic Product (GDP)

* Broad Money Supply (BM)

* Exchange Rate (EX)


**Methods Used:**

* Johansen Cointegration Test
* Vector AutoRegression (VAR) Model
* Impulse Response Functions (IRF)


 ### 2."Forecasting Monthly Inflation in Bangladesh: A Seasonal Autoregressive Moving Average (SARIMA) Approach"
   - Link: https://ojs.tripaledu.com/jefa/article/view/85/95
   - Description: Used Johansen Cointegration test to examine long-term relationships among inflation, GDP, money supply, and exchange rate.
     Employed a VAR (Vector AutoRegression) model to analyze causal relationships among these variables.

**Methods Used:**

* Applied SARIMA (Seasonal ARIMA) model.
* Selected the SARIMA (2,0,0) × (1,0,1)12 model .


## Insights on Variables:
* CPI is central in both papers as the primary measure of inflation.
* The first paper focuses on macroeconomic drivers (GDP, money supply, exchange rate) for causal analysis, while the second paper emphasizes seasonality in monthly CPI data for short-term forecasting.


## Dataset Details
The project will use both local and global economic data sources to build a comprehensive dataset. Key data sources include:
* Kaggle: Bangladesh Economic Indicators (1980 - 2019).

    link:  https://www.kaggle.com/datasets/salehahmedrony/bangladesh-economic-indicators-1980-2019?resource=download
* Kaggle: Economic Trends of Bangladesh.

    Link:https://www.kaggle.com/datasets/shreyaskeote23/bangladesh-economy
* **We are also looking for World Bank Data and Bangladesh Bank Data**

**Note: We will integrate multiple variable from different dataset to customize our own dataset**



### Estimated Features in the Dataset
1. Consumer Price Index (CPI) (target variable)
2. Unemployment Rate
3. Exchange Rates (USD to BDT)
4. Crude Oil Prices
5. Vat on Essential Goods
6. Interest Rates
7. Government Spending
8. Import/Export Values
9. International Loan
10.Inflation Previous Data

### Data Frequency
Monthly/Quarterly/yearly data spanning at least 10–20 years for meaningful analysis.

## Models to Build
The following models will be implemented and evaluated:

**1. Time Series Models**
* ARIMA (AutoRegressive Integrated Moving Average)
* SARIMA (Seasonal ARIMA)
* VAR (Vector AutoRegression)

**2. Machine Learning Regression Models**
* Linear Regression: Basic benchmark model.
* Random Forest Regressor.
* Gradient Boosting Models.
* XGBoost.
* Support Vector Machines (SVM): Regression with the kernel trick to handle non-linear patterns.

**3.Deep Learning Models**
* Long Short-Term Memory (LSTM)

## Novelty of the Project
1. **Localized Focus**
2. **Hybrid Model Approach**
3. **Huge Number of Features** 


## Challenges

1. **Data Availability and Quality:**
   
2. **Feature Engineering:**
   
3. **Model Complexity:**
   
4. **Interpretability:**
  
6. **Validation and Generalization of Models:**
  

