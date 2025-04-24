# GridGenius: Modeling Pipeline and Results

**Objective:** Forecast daily energy consumption based on historical data.
**Task Type:** Supervised Learning, Time-Series Regression.

**General Pipeline:**
1.  **Defining the Problem:** Forecasting daily energy demand.
2.  **Data Preparation:** Collection, feature engineering, preprocessing (handling missing/duplicates, outliers), transformation (scaling/encoding).
3.  **Data Split:** Splitting data into Training (80%) and Testing (20%) sets. A validation set might be created from the training set if needed for hyperparameter tuning.
4.  **Model Selection:** Choosing appropriate ML and DL models.
5.  **Model Training:** Training selected models on the training data, optimizing hyperparameters.
6.  **Evaluation:** Assessing model performance on the testing set using various metrics.
7.  **Deployment:** Integrating the best model(s) into the website/API.
8.  **Documentation:** Recording steps, writing papers, releasing code.

**Models Selected & Trained:**
A hybrid approach was considered, potentially combining multiple models. Initially, five individual models were trained and evaluated on 4 different iterations of the preprocessed dataset:
*   Linear Regression
*   Random Forest (RF)
*   Support Vector Regressor (SVM / SVR)
*   Gradient Boosting
*   XGBoost

(LSTM and ARIMA were mentioned as potential DL models but initial results focused on the above five).

**Training Process:**
*   Each model was trained separately.
*   Hyperparameter optimization techniques like Grid Search or Bayesian Optimization were planned.

**Evaluation Metrics:**
*   **R2 Score (Coefficient of Determination):** Primary metric (higher is better).
*   **MAE (Mean Absolute Error):** Lower is better.
*   **MSE (Mean Square Error):** Lower is better.
*   **RMSE (Root Mean Square Error):** Lower is better.
*   MAPE (Mean Absolute Percentage Error) was also considered.

**Initial Results Summary:**
*   Evaluations were performed on 4 dataset variations (combinations of MinMaxScaler/StandardScaler and IQR/Z-Score outlier removal).
*   **Random Forest** and **XGBoost** consistently performed the best across the dataset iterations.
*   They achieved high **R2 scores (~0.89 - 0.90)**.
*   They also demonstrated the lowest error metrics (MAE, MSE, RMSE).
*   The best results highlighted were primarily from dataset iterations 'energy_iter13a' and 'energy_iter13b' (using MinMaxScaler).

**Conclusion:** Random Forest and XGBoost were initially identified as the most accurate models for demand prediction based on these experiments.