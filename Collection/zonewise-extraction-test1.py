import fitz
import re
import pandas as pd

pdf_path = 'pdf_path'
doc = fitz.open(pdf_path)

text = ""
for page in doc:
    text += page.get_text()

doc.close()

date_pattern = re.search(r'Date\s*:\s*(\d{2}\.\d{2}\.\d{2})', text)
report_date = date_pattern.group(1) if date_pattern else "Unknown"

print(f"Report Date: {report_date}\n")

zones = ["Dhaka", "Chattogram", "Cumilla", "Mymensing", "Sylhet", "Khulna", "Barishal", "Rajshahi", "Rangpur"]

zone_data = []
for zone in zones:
    
    pattern = re.compile(rf'({zone} Zone Total.*?(\d+\.\d+|\d+).*\n.*?(\d+\.\d+|\d+).*\n.*?(\d+\.\d+|\d+).*\n.*?(\d+\.\d+|\d+))', re.DOTALL)
    match = pattern.search(text)
    if match:
        print(f"Matched text for {zone}:\n{match.group(0)}\n")
        numbers = re.findall(r'(\d+\.\d+|\d+)', match.group(0))
        if len(numbers) >= 6:
            day_peak = float(numbers[4])
            evening_peak = float(numbers[5])
            zone_data.append([report_date, zone, day_peak, evening_peak])

df_zones = pd.DataFrame(zone_data, columns=["Report Date", "Zone", "Probable Day Peak (MW)", "Probable Evening Peak (MW)"])

print(df_zones)