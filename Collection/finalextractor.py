import fitz  # PyMuPDF
import re
import pandas as pd
import os
import argparse
from datetime import datetime

# --- Configuration ---

# Hardcoded holiday dates (ensure this list is comprehensive and up-to-date)
# Copied from extractionHolidays.py and added a few placeholders for 2025
HOLIDAY_DATES_STR = [
    # 2020
    "2020-01-03", "2020-01-10", "2020-01-17", "2020-01-24", "2020-01-31", "2020-02-07", "2020-02-14", "2020-02-21",
    "2020-02-28", "2020-03-06", "2020-03-13", "2020-03-20", "2020-03-26", "2020-03-27", "2020-04-03", "2020-04-10",
    "2020-04-14", "2020-04-17", "2020-04-24", "2020-05-01", "2020-05-08", "2020-05-15", "2020-05-22", "2020-05-29",
    "2020-06-05", "2020-06-12", "2020-06-19", "2020-06-26", "2020-07-03", "2020-07-10", "2020-07-17", "2020-07-24",
    "2020-07-31", "2020-08-07", "2020-08-14", "2020-08-15", "2020-08-21", "2020-08-28", "2020-09-04", "2020-09-11",
    "2020-09-18", "2020-09-25", "2020-10-02", "2020-10-09", "2020-10-16", "2020-10-23", "2020-10-30", "2020-11-06",
    "2020-11-13", "2020-11-20", "2020-11-27", "2020-12-04", "2020-12-11", "2020-12-18", "2020-12-25",
    # 2021
    "2021-01-01", "2021-01-08", "2021-01-15", "2021-01-22", "2021-01-29", "2021-02-05", "2021-02-12", "2021-02-19",
    "2021-02-26", "2021-03-05", "2021-03-12", "2021-03-19", "2021-03-26", "2021-04-02", "2021-04-09", "2021-04-14",
    "2021-04-16", "2021-04-23", "2021-04-30", "2021-05-07", "2021-05-14", "2021-05-21", "2021-05-28", "2021-06-04",
    "2021-06-11", "2021-06-18", "2021-06-25", "2021-07-02", "2021-07-09", "2021-07-16", "2021-07-23", "2021-07-30",
    "2021-08-06", "2021-08-13", "2021-08-15", "2021-08-20", "2021-08-27", "2021-09-03", "2021-09-10", "2021-09-17",
    "2021-09-24", "2021-10-01", "2021-10-08", "2021-10-15", "2021-10-22", "2021-10-29", "2021-11-05", "2021-11-12",
    "2021-11-19", "2021-11-26", "2021-12-03", "2021-12-10", "2021-12-17", "2021-12-24", "2021-12-31",
    # 2022
    "2022-01-07", "2022-01-14", "2022-01-21", "2022-01-28", "2022-02-04", "2022-02-11", "2022-02-18", "2022-02-25",
    "2022-03-04", "2022-03-11", "2022-03-18", "2022-03-25", "2022-04-01", "2022-04-08", "2022-04-14", "2022-04-15",
    "2022-04-22", "2022-04-29", "2022-05-06", "2022-05-13", "2022-05-20", "2022-05-27", "2022-06-03", "2022-06-10",
    "2022-06-17", "2022-06-24", "2022-07-01", "2022-07-08", "2022-07-15", "2022-07-22", "2022-07-29", "2022-08-05",
    "2022-08-12", "2022-08-19", "2022-08-26", "2022-09-02", "2022-09-09", "2022-09-16", "2022-09-23", "2022-09-30",
    "2022-10-07", "2022-10-14", "2022-10-21", "2022-10-28", "2022-11-04", "2022-11-11", "2022-11-18", "2022-11-25",
    "2022-12-02", "2022-12-09", "2022-12-16", "2022-12-23", "2022-12-30",
    # 2023
    "2023-01-06", "2023-01-13", "2023-01-20", "2023-01-27", "2023-02-03", "2023-02-10", "2023-02-17", "2023-02-24",
    "2023-03-03", "2023-03-10", "2023-03-17", "2023-03-24", "2023-03-31", "2023-04-07", "2023-04-14", "2023-04-21",
    "2023-04-28", "2023-05-05", "2023-05-12", "2023-05-19", "2023-05-26", "2023-06-02", "2023-06-09", "2023-06-16",
    "2023-06-23", "2023-06-30", "2023-07-07", "2023-07-14", "2023-07-21", "2023-07-28", "2023-08-04", "2023-08-11",
    "2023-08-18", "2023-08-25", "2023-09-01", "2023-09-08", "2023-09-15", "2023-09-22", "2023-09-29", "2023-10-06",
    "2023-10-13", "2023-10-20", "2023-10-27", "2023-11-03", "2023-11-10", "2023-11-17", "2023-11-24", "2023-12-01",
    "2023-12-08", "2023-12-15", "2023-12-22", "2023-12-29",
    # 2024
    "2024-01-05", "2024-01-12", "2024-01-19", "2024-01-26", "2024-02-02", "2024-02-09", "2024-02-16", "2024-02-23",
    "2024-03-01", "2024-03-08", "2024-03-15", "2024-03-22", "2024-03-29", "2024-04-05", "2024-04-12", "2024-04-19",
    "2024-04-26", "2024-05-03", "2024-05-10", "2024-05-17", "2024-05-24", "2024-05-31", "2024-06-07", "2024-06-14",
    "2024-06-21", "2024-06-28", "2024-07-05", "2024-07-12", "2024-07-19", "2024-07-26", "2024-08-02", "2024-08-09",
    "2024-08-16", "2024-08-23", "2024-08-30", "2024-09-06", "2024-09-13", "2024-09-20", "2024-09-27", "2024-10-04",
    "2024-10-11", "2024-10-18", "2024-10-25", "2024-11-01", "2024-11-08", "2024-11-15", "2024-11-22", "2024-11-29",
    "2024-12-06", "2024-12-13", "2024-12-20", "2024-12-27",
    # 2025 (Added a few examples, this list would need to be maintained for future years)
    "2025-01-01", "2025-01-03", "2025-01-10", "2025-03-21", "2025-04-18", "2025-05-01", "2025-06-01", # Sample: 01-06-2025 is a Sunday
    "2025-12-25", "2025-12-26"
]
HOLIDAY_DATES_SET = set([date.strip() for date in HOLIDAY_DATES_STR])

ZONES = ["Dhaka", "Chattogram", "Cumilla", "Mymensing", "Sylhet", "Khulna", "Barishal", "Rajshahi", "Rangpur"]

# --- Helper Functions ---
def safe_search(pattern, text, group_num=1, type_cast=str, default=None, flags=0):
    match = re.search(pattern, text, flags)
    if match:
        try:
            value = match.group(group_num)
            # Strip whitespace before casting, especially for numbers
            value_stripped = value.strip() if value else ""
            if not value_stripped: # Handle empty string after strip
                return default
            if type_cast == bool:
                return True # Or specific logic, e.g., value_stripped.lower() in ['yes', 'true']
            return type_cast(value_stripped)
        except (IndexError, ValueError, TypeError):
            return default
    return default

def convert_date_format(date_str_dmy_short_year, default=None):
    """Converts DD.MM.YY to YYYY-MM-DD."""
    if not date_str_dmy_short_year:
        return default
    try:
        return datetime.strptime(date_str_dmy_short_year, "%d.%m.%y").strftime("%Y-%m-%d")
    except ValueError:
        return default

def extract_numbers_from_text_block(text_block, num_count):
    """Extracts a specific number of floating point or integer numbers from a text block."""
    if not text_block:
        return [None] * num_count
    # Regex to find numbers, including negative or decimal
    numbers_found = re.findall(r'(-?\d+\.\d+|-?\d+)', text_block)
    result = []
    for i in range(num_count):
        try:
            result.append(float(numbers_found[i]))
        except (IndexError, ValueError):
            result.append(None)
    return result

# --- Main Extraction Logic ---
def extract_data_from_pdf_text(text, pdf_filename):
    data = {"FileName": pdf_filename}

    # Normalize whitespace for easier regex matching
    text = re.sub(r'\s+', ' ', text)

    # 1. General Report Info
    data['ReportDate_Raw'] = safe_search(r'Date\s*:\s*(\d{2}\.\d{2}\.\d{2})', text)
    data['ReportDate'] = convert_date_format(data['ReportDate_Raw'])
    data['DayOfWeek'] = safe_search(r'Day\s*:\s*(\w+)', text, group_num=1)
    data['ReportMonth'] = safe_search(r'Month\s*([A-Za-z]+)\s*,\s*\d{4}', text, group_num=1)

    data['ProbableMaxDemand_MW_Forecast'] = safe_search(r'Probable Maximum Demand\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)
    # Handle potential "MW MW"
    gen_forecast_match = re.search(r'Probable Maximum Generation\s*:\s*([\d\.]+)\s*MW(?: MW)?', text)
    if gen_forecast_match:
        data['ProbableMaxGeneration_MW_Forecast'] = safe_search(r'([\d\.]+)', gen_forecast_match.group(0), type_cast=float)
    else:
        data['ProbableMaxGeneration_MW_Forecast'] = None


    gross_total_match = re.search(r"Gross\s*Total\s*((?:-?\d+\.?\d*\s*)+)", text)
    if gross_total_match:
        gross_total_numbers_str = gross_total_match.group(1).strip()
        gross_numbers = extract_numbers_from_text_block(gross_total_numbers_str, 8) # Expecting at least 6, up to 8 numbers
        data['GrossTotal_ProbableDayPeakGeneration_MW'] = gross_numbers[4]
        data['GrossTotal_ProbableEveningPeakGeneration_MW'] = gross_numbers[5]
    else:
        data['GrossTotal_ProbableDayPeakGeneration_MW'] = None
        data['GrossTotal_ProbableEveningPeakGeneration_MW'] = None

    for zone in ZONES:
        pattern_zone_total = re.compile(rf'{re.escape(zone)}\s*Zone\s*Total\s*(.*?)', re.IGNORECASE)
        # Find the start of the zone total line, then extract numbers
        # Need to capture until the next "Zone Total" or end of table section
        # This simplified version captures numbers immediately following "Zone Total" on its line
        match_zone_line = pattern_zone_total.search(text)
        day_peak_val, evening_peak_val = None, None
        if match_zone_line:
            # Extract numbers from the matched part of the line
            # Example: Dhaka Zone Total 6081 5910 2053 2434 5099 5304 2389 480
            # The numbers typically are: Inst Cap, Derated, Actual Day, Actual Eve, Prob Day, Prob Eve, Shortfall, Machines s/d
            # We need the 5th and 6th numbers (0-indexed: 4 and 5) from this sequence on the line
            numbers_from_line = extract_numbers_from_text_block(match_zone_line.group(1), 8)
            if len(numbers_from_line) >= 6:
                 day_peak_val = numbers_from_line[4]
                 evening_peak_val = numbers_from_line[5]
        data[f'{zone}_ProbableDayPeakGen_MW'] = day_peak_val
        data[f'{zone}_ProbableEveningPeakGen_MW'] = evening_peak_val

    # --- Actual Data from Previous Day (Section C) ---
    data['PreviousReportDate_Raw'] = safe_search(r'Actual data of\s*(\d{2}\.\d{2}\.\d{2})', text)
    data['PreviousReportDate'] = convert_date_format(data['PreviousReportDate_Raw'])

    data['Actual_MaxDemandEvePeak_MW'] = safe_search(r'Max\. Demand at eve\. peak \(Generation end\)\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)
    data['Actual_EveningPeakGeneration_MW'] = safe_search(r'Evening-peak Generation \(Generation end\)\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)
    data['Actual_HighestGeneration_MW'] = safe_search(r'Highest Generation \(Generation end\)\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)
    data['Actual_DayPeakDemand_MW'] = safe_search(r'Day Peak Demand\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)
    data['Actual_DayPeakGeneration_MW'] = safe_search(r'Day-peak Generation \(Generation end\)\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)
    data['Actual_MinimumGeneration_MW'] = safe_search(r'Minimum Generation \(Generation end\)\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)

    data['Actual_Shortfall_GasLF_MW'] = safe_search(r'Gas/LF limitation\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)
    data['Actual_Shortfall_Coal_MW'] = safe_search(r'Coal supply Limitation\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)
    data['Actual_Shortfall_KaptaiWater_MW'] = safe_search(r'Low water level in Kaptai lake\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)
    data['Actual_Shortfall_PlantShutdown_MW'] = safe_search(r'Plants under shut down/maintenance\s*:\s*([\d\.]+)\s*MW', text, type_cast=float)

    data['Actual_TotalEnergy_GenImport_MKWh'] = safe_search(r'Total Energy \(Generation \+ Import\)\s*:\s*([\d\.]+)\s*MKWh', text, type_cast=float)
    data['Actual_Energy_Gas_MKWh'] = safe_search(r'By Gas\s*=\s*([\d\.]+)\s*MKWH', text, type_cast=float, flags=re.IGNORECASE)
    data['Actual_Energy_Oil_MKWh'] = safe_search(r'By Oil\s*=\s*([\d\.]+)\s*MKWh', text, type_cast=float, flags=re.IGNORECASE)
    data['Actual_Energy_Coal_MKWh'] = safe_search(r'By Coal\s*=\s*([\d\.]+)\s*MKWH', text, type_cast=float, flags=re.IGNORECASE)
    data['Actual_Energy_HydroWind_MKWh'] = safe_search(r'Hydro&Wind\s*=\s*([\d\.]+)\s*MKWh', text, type_cast=float, flags=re.IGNORECASE)
    data['Actual_Energy_Solar_MKWh'] = safe_search(r'By Solar\s*=\s*([\d\.]+)\s*MKWH', text, type_cast=float, flags=re.IGNORECASE)
    data['Actual_Energy_Imported_MKWh'] = safe_search(r'Imported\s*=\s*([\d\.]+)\s*MKWh', text, type_cast=float, flags=re.IGNORECASE) # Case for MKWh
    data['Actual_TotalGasSupplied_MMCFD'] = safe_search(r'Total Gas Supplied\s*:\s*([\d\.]+)\s*MMCFD', text, type_cast=float)
    data['Actual_MaxTemperature_C'] = safe_search(r'Maximum Temperature\s*:\s*([\d\.]+)', text, type_cast=float)

    # Zone-wise Actual Demand/Supply/Loadshed (Section C) - More robust parsing
    actual_zonal_data_map = {}
    actual_zonal_table_header = r"Zone wise Demand and Load-shed at Evening Peak \(Sub-station end\)\s*:?"
    # Try to find the block of text for this table
    table_block_match = re.search(actual_zonal_table_header + r"(.*?)(11\.\s*Fuel cost:|Forecast of|\(D\)\s*Forecast of)", text, re.DOTALL | re.IGNORECASE)
    search_text_for_actual_zone = table_block_match.group(1) if table_block_match else text

    patterns_actual_zonal = {
        ("Dhaka", "Mymensingh"): r"Dhaka\s*([\d\.]+)\s*([\d\.]+)\s*([\d\.]+)\s*Mymensingh\s*([\d\.]+)\s*([\d\.]+)\s*([\d\.]+)",
        ("Chattogram", "Sylhet"): r"Chattogram\s*([\d\.]+)\s*([\d\.]+)\s*([\d\.]+)\s*Sylhet\s*([\d\.]+)\s*([\d\.]+)\s*([\d\.]+)",
        ("Khulna", "Barishal"): r"Khulna\s*([\d\.]+)\s*([\d\.]+)\s*([\d\.]+)\s*Barishal\s*([\d\.]+)\s*([\d\.]+)\s*([\d\.]+)",
        ("Rajshahi", "Rangpur"): r"Rajshahi\s*([\d\.]+)\s*([\d\.]+)\s*([\d\.]+)\s*Rangpur\s*([\d\.]+)\s*([\d\.]+)\s*([\d\.]+)"
    }

    for (zone1, zone2), pattern in patterns_actual_zonal.items():
        match = re.search(pattern, search_text_for_actual_zone, re.IGNORECASE)
        if match:
            g = match.groups()
            try:
                actual_zonal_data_map[zone1] = [float(val) if val else None for val in g[0:3]]
                actual_zonal_data_map[zone2] = [float(val) if val else None for val in g[3:6]]
            except (ValueError, TypeError): # Handle if a value is not a number
                 actual_zonal_data_map[zone1] = [None,None,None] # Or log error
                 actual_zonal_data_map[zone2] = [None,None,None]


    for zone_name in ZONES:
        vals = actual_zonal_data_map.get(zone_name, [None, None, None])
        data[f'{zone_name}_Actual_Demand_MW'] = vals[0]
        data[f'{zone_name}_Actual_Supply_MW'] = vals[1]
        data[f'{zone_name}_Actual_LoadShed_MW'] = vals[2]

    # --- Forecast Data for Current Day (Section D) ---
    data['Forecast_ProbableLoadShed_MW'] = safe_search(r'Probable Load Shed\s*:\s*([\d\.]+)\s*(?:MW|At evening peak|$)', text, type_cast=float)
    data['Forecast_TotalEnergyGeneration_MKWh'] = safe_search(r'Probable Total Energy Generation\s*:\s*([\d\.]+)\s*MKWHr', text, type_cast=float, flags=re.IGNORECASE)
    data['Forecast_MaxTemperature_C'] = safe_search(r'Probable Maximum Temperature\s*:\s*([\d\.]+)\s*°C', text, type_cast=float)

    return data

def process_pdf_file(pdf_path):
    """Extracts text from a PDF and then processes it."""
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Using "text" for standard text extraction. If PDFs are image-based, OCR would be needed.
            full_text += page.get_text("text") + "\n"
        doc.close()
        
        if not full_text.strip():
            print(f"Warning: No text could be extracted from {pdf_path}. It might be an image-only PDF or empty.")
            return None
            
        return extract_data_from_pdf_text(full_text, os.path.basename(pdf_path))
    except Exception as e:
        print(f"Error processing PDF file {pdf_path}: {e}")
        return None

# --- Main Execution ---
def main():
    parser = argparse.ArgumentParser(description="Extract data from Bangladesh Power Development Board PDF reports.")
    parser.add_argument("input_path", help="Path to a single PDF file or a folder containing PDF files.")
    parser.add_argument("output_csv", help="Path to save the extracted data as a CSV file.")
    args = parser.parse_args()

    all_extracted_data = []

    if os.path.isfile(args.input_path):
        if args.input_path.lower().endswith(".pdf"):
            print(f"Processing single file: {args.input_path}")
            data = process_pdf_file(args.input_path)
            if data:
                all_extracted_data.append(data)
        else:
            print(f"Error: Input file {args.input_path} is not a PDF.")
            return
    elif os.path.isdir(args.input_path):
        print(f"Processing folder: {args.input_path}")
        for filename in sorted(os.listdir(args.input_path)):
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(args.input_path, filename)
                print(f"  Processing: {filename}")
                data = process_pdf_file(pdf_path)
                if data:
                    all_extracted_data.append(data)
    else:
        print(f"Error: Input path {args.input_path} is not a valid file or folder.")
        return

    if not all_extracted_data:
        print("No data extracted. Output CSV will not be created.")
        return

    df = pd.DataFrame(all_extracted_data)

    if 'ReportDate' in df.columns:
        # Ensure ReportDate is string for holiday set lookup, handle NaT/None
        df['IsHoliday'] = df['ReportDate'].apply(
            lambda x: 'Yes' if pd.notna(x) and str(x) in HOLIDAY_DATES_SET else 'No'
        )
    else:
        print("Warning: 'ReportDate' column not found. 'IsHoliday' column will be set to 'No'.")
        df['IsHoliday'] = 'No'

    cols = df.columns.tolist()
    preferred_order = ['FileName', 'ReportDate_Raw', 'ReportDate', 'IsHoliday', 'DayOfWeek', 'ReportMonth']
    # Ensure all preferred columns exist before trying to reorder
    existing_preferred = [p for p in preferred_order if p in cols]
    new_cols_order = existing_preferred + [c for c in cols if c not in existing_preferred]
    df = df[new_cols_order]

    try:
        df.to_csv(args.output_csv, index=False, encoding='utf-8')
        print(f"\nExtraction complete. Data saved to {args.output_csv}")
    except Exception as e:
        print(f"Error saving CSV to {args.output_csv}: {e}")

if __name__ == "__main__":
    main()