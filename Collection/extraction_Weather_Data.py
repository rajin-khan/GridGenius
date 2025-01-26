
from google.colab import files
uploaded = files.upload()

from google.colab import files
uploaded = files.upload()

from google.colab import files
uploaded = files.upload()

from google.colab import files
uploaded = files.upload()

from google.colab import files
uploaded = files.upload()

import pandas as pd

# rename
csv_files = ['t2020.csv', 't2021.csv', 't2022.csv', 't2023.csv', 't2024.csv']

# merge the CSV files into a single dataframe
merged_data = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Optionally, sort the data by the 'Date' column
merged_data['datetime'] = pd.to_datetime(merged_data['datetime'])
merged_data = merged_data.sort_values(by='datetime')

# Save the merged data into a new CSV file
merged_data.to_csv('merged_temperature_data.csv', index=False)

from google.colab import files
files.download('merged_temperature_data.csv')

import pandas as pd

df = pd.read_csv('merged_temperature_data.csv')

# List the columns that we want to keep
columns_to_keep = ['datetime', 'tempmax', 'tempmin', 'temp', 'feelslike','humidity']  # Update column names as needed


df_filtered = df[columns_to_keep]

print(df_filtered.head())

# Save the filtered data into a new CSV file
df_filtered.to_csv('filtered_temp_file.csv', index=False)


from google.colab import files
files.download('filtered_temp_file.csv')

