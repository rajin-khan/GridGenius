import pandas as pd
from google.colab import files


uploaded = files.upload()


file_name = list(uploaded.keys())[0]
df = pd.read_csv(file_name)


print(df.head())


drop_columns = ['tempmax', 'tempmin', 'feelslike', 'humidity']
df = df.drop(columns=drop_columns)
print("\nDropped ")

# Rename columns
rename_columns = {
    'Report_Date': 'Date',
    'Day_ProbPeakGen(MW)': 'DayPeakGen(MW)',
    'Evening_ProbPeakGen(MW)': 'EveningPeakGen(MW)',
    'ProbMaxDemand(MW)': 'MaxDemand(MW)',
    'ProbMaxGen(MW)': 'MaxGeneration(MW)',
    'temp': 'Temperature',
    'year': 'Year',
    'month': 'Month',
    'season': 'Season'
}
df = df.rename(columns=rename_columns)
print("\nRenamed ")

print(df.head())

output_file_name = "energy_iter5.csv"
df.to_csv(output_file_name, index=False)

from google.colab import files
files.download(output_file_name)