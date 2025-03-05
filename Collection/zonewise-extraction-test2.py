import fitz
import re
import pandas as pd
import os

folder_path = './data_pdfs/'

all_data = []

for pdf_file in os.listdir(folder_path):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"Processing: {pdf_file}")

        doc = fitz.open(pdf_path)

        text = ""
        for page in doc:
            text += page.get_text()

        doc.close()

        date_pattern = re.search(r'Date\s*:\s*(\d{2}\.\d{2}\.\d{2})', text)
        report_date = date_pattern.group(1) if date_pattern else "Unknown"

        print(f"Report Date: {report_date}\n")

        zones = ["Dhaka", "Chattogram", "Cumilla", "Mymensing", "Sylhet", "Khulna", "Barishal", "Rajshahi", "Rangpur"]

        for zone in zones:
            pattern = re.compile(rf'({zone} Zone Total.*?(\d+\.\d+|\d+).*\n.*?(\d+\.\d+|\d+).*\n.*?(\d+\.\d+|\d+).*\n.*?(\d+\.\d+|\d+))', re.DOTALL)
            match = pattern.search(text)
            if match:
                numbers = re.findall(r'(\d+\.\d+|\d+)', match.group(0))
                if len(numbers) >= 6:
                    day_peak = float(numbers[4])
                    evening_peak = float(numbers[5])
                    all_data.append([pdf_file, report_date, zone, day_peak, evening_peak])

df_all_zones = pd.DataFrame(all_data, columns=["File Name", "Report Date", "Zone", "Probable Day Peak (MW)", "Probable Evening Peak (MW)"])

print(df_all_zones)

df_all_zones.to_csv('/Users/rajin/Developer/zonewise_iter1.csv', index=False)
print("Data saved to 'zonewise_generation_data.csv'")