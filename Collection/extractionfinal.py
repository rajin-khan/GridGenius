import os
import PyPDF2
import re
import pandas as pd

# Directory containing PDF files
input_directory = "summary_pdfs"
output_csv = "extracted_energy_data.csv"

# Function to extract relevant data from a PDF
def extract_relevant_data(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

            # Clean text to remove excessive spaces and non-ASCII characters
            cleaned_text = re.sub(r'\s+', ' ', text)

            # Regex to extract Gross Total values for probable peak generation
            peak_pattern = r"Gross\s*Total\s+(\d{4,5})\s+(\d{4,5})\s+(\d{4,5})\s+(\d{4,5})\s+(\d{4,5})\s+(\d{4,5})"
            peak_match = re.search(peak_pattern, cleaned_text)

            # Regex to extract the report date
            date_pattern = r"Date\s*[:\-\s]*(\d{2}\.\d{2}\.\d{2})"
            date_match = re.search(date_pattern, cleaned_text)

            # Regex to extract Probable Maximum Demand (MW)
            demand_pattern = r"Probable Maximum Demand\s*:\s*(\d{3,5})\s*MW"
            demand_match = re.search(demand_pattern, cleaned_text)

            # Regex to extract Probable Maximum Generation (MW)
            generation_pattern = r"Probable Maximum Generation\s*:\s*(\d{3,5})\s*MW"
            generation_match = re.search(generation_pattern, cleaned_text)

            if peak_match and date_match and demand_match and generation_match:
                report_date = date_match.group(1)
                day_peak = peak_match.group(5)
                evening_peak = peak_match.group(6)
                probable_demand = demand_match.group(1)
                probable_generation = generation_match.group(1)

                return {
                    "File_Name": os.path.basename(pdf_path),
                    "Report_Date": report_date,
                    "Day_Probable_Peak_Generation": day_peak,
                    "Evening_Probable_Peak_Generation": evening_peak,
                    "Probable_Maximum_Demand_MW": probable_demand,
                    "Probable_Maximum_Generation_MW": probable_generation
                }
            else:
                print(f"No relevant data found in: {pdf_path}")
                return None

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

# Function to process all PDFs in the specified folder
def process_pdf_folder(folder_path, output_csv):
    extracted_data = []

    # Loop through all PDF files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")
            data = extract_relevant_data(pdf_path)
            if data:
                extracted_data.append(data)

    # Convert extracted data to a Pandas DataFrame and save to CSV
    if extracted_data:
        df = pd.DataFrame(extracted_data)
        df.to_csv(output_csv, index=False)
        print(f"\nExtraction complete. Data saved to {output_csv}")
    else:
        print("\nNo valid data extracted.")

# Run the script
if __name__ == "__main__":
    process_pdf_folder(input_directory, output_csv)