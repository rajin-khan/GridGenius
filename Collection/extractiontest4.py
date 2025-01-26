
import pandas as pd
from google.colab import files

# Upload the file
uploaded = files.upload()

# Load the dataset
file_name = list(uploaded.keys())[0]
main_merged_updated = pd.read_csv(file_name)

main_merged_updated['Report_Date'] = pd.to_datetime(main_merged_updated['Report_Date'], format='%Y-%m-%d')

# Extract year and month
main_merged_updated['year'] = main_merged_updated['Report_Date'].dt.year
main_merged_updated['month'] = main_merged_updated['Report_Date'].dt.month

# Define a function to execute
def get_season(month):
    if month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8, 9, 10]:
        return 'Monsoon'
    elif month in [11, 12, 1, 2]:
        return 'Winter'

#  create  'season' column
main_merged_updated['season'] = main_merged_updated['month'].apply(get_season)



main_merged_updated.to_csv('energy_iter4.csv', index=False)
print("Updated dataset saved as 'energy_iter4.csv'")

files.download('energy_iter4.csv')