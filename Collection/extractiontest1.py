import PyPDF2
import re

# Path to the provided PDF file
pdf_path = "./poweroptim/summary_pdfs/5029report.pdf"

def extract_relevant_data(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

            # Clean text to remove excessive spaces and non-ASCII characters
            cleaned_text = re.sub(r'\s+', ' ', text)

            # Regex pattern to extract the probable peak generation values from the "Gross Total" row
            peak_pattern = r"Gross\s*Total\s+(\d{4,5})\s+(\d{4,5})\s+(\d{4,5})\s+(\d{4,5})\s+(\d{4,5})\s+(\d{4,5})"
            peak_match = re.search(peak_pattern, cleaned_text)

            # Regex to extract the report date
            date_pattern = r"Date\s*[:\-\s]*(\d{2}\.\d{2}\.\d{2})"
            date_match = re.search(date_pattern, cleaned_text)

            if peak_match and date_match:
                report_date = date_match.group(1)
                day_peak = peak_match.group(5)
                evening_peak = peak_match.group(6)

                return {
                    "Report_Date": report_date,
                    "Day_Probable_Peak_Generation": day_peak,
                    "Evening_Probable_Peak_Generation": evening_peak
                }
            else:
                return "No relevant data found."

    except Exception as e:
        return f"Error processing PDF: {e}"

# Extract data from the provided PDF
extracted_info = extract_relevant_data(pdf_path)

# Print extracted information
print(extracted_info)
