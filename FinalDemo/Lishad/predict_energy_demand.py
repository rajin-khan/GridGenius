import sys
import numpy as np
import joblib

# Load model and scaler
model = joblib.load("energy_model.pkl")
scaler = joblib.load("scaler.pkl")


day = int(sys.argv[1])
year = int(sys.argv[2])
month = int(sys.argv[3])
season = int(sys.argv[4])
isholiday = int(sys.argv[5])
temp_raw = float(sys.argv[6])  


# Normalize the raw temperature using scaler
temp_min = scaler.data_min_[2]  
temp_range = scaler.data_range_[2]
temp_scaled = (temp_raw - temp_min) / temp_range



# Create input array with 6 features
X_input = np.array([[temp_scaled, year, month, season, isholiday, day]])


# Predict using model
scaled_prediction = model.predict(X_input)

# Inverse transform
demand_min = scaler.data_min_[0]
demand_range = scaler.data_range_[0]
predicted_demand = scaled_prediction[0] * demand_range + demand_min

# Output 
print(predicted_demand)
