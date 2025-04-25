# GridGenius: Transformer Model for Prediction

**Novelty:** GridGenius utilizes a Transformer Model for its energy demand predictions.

**Model Architecture:**
*   The model is a **Transformer Encoder-based Regression Model**.
*   It's a fully connected Transformer-based Neural Network.
*   **Goal:** Predict Daily Energy Demand based on various inputs (Temperature, Holiday status, historical Energy Generation, Date components etc.).

**Key Components:**
1.  **Input Layer:**
    *   Takes input features (e.g., Temperature, Date parts).
    *   Features pass through a **linear layer** to transform them into a high-dimensional representation suitable for the transformer.
2.  **Transformer Encoder Layer(s):**
    *   This is the core, containing multiple transformer encoder layers.
    *   Each layer uses **multi-head self-attention** to analyze relationships and dependencies between input features (e.g., how Temperature and Holiday status *together* affect demand).
    *   Includes **positional encoding** to help the model understand the sequence of inputs, crucial for Time-Series Forecasting.
    *   Hyperparameters (like number of layers, heads, dimensions) are tuned through multiple trials.
3.  **Output Layer:**
    *   A final **linear layer** converts the learned representation from the encoder layers into a single numerical output.
    *   This output represents the **Predicted Power Demand (MW)**.

**Current Performance:**
*   Work on optimizing the Transformer model is ongoing.
*   As of the latest update, the model achieves:
    *   **R2 Score: 0.82**
    *   **MAE: 0.06** (very low)
    *   **RMSE: 0.08** (very low)
    (Note: These metrics are likely on scaled data, hence the low MAE/RMSE values).