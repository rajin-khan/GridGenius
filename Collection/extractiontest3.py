

import pandas as pd

# Load the first CSV file
file1 = pd.read_csv('cleaned_energy_datewise.csv')  # first file
file2 = pd.read_csv('merged_temperature_data.csv')  #  second file

# Convert the 'Report_Date' in file1 to datetime format
file1['Report_Date'] = pd.to_datetime(file1['Report_Date'], format='%d-%m-%Y')

# Convert the 'datetime' in file2 to datetime format
file2['datetime'] = pd.to_datetime(file2['datetime'], format='%Y-%m-%d')

# Select specific features from file2
selected_features = ['datetime', 'tempmax', 'tempmin', 'temp', 'feelslike', 'humidity']

file2_selected = file2[selected_features]

# Merge the two files on matching dates, keeping all features from file1
merged_df = pd.merge(file1, file2_selected, left_on='Report_Date', right_on='datetime', how='inner')

# Drop the redundant 'datetime' column after merging
merged_df.drop(columns=['datetime'], inplace=True)

# Save the merged result to a new CSV file
merged_df.to_csv('merged_file.csv', index=False)