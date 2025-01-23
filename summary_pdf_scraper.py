import os
import requests
import urllib3
from bs4 import BeautifulSoup

# Disable SSL warnings to avoid interruptions
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base URL for the daily generation archive pages
BASE_URL = "https://misc.bpdb.gov.bd/daily-generation-archive?page="

# Directory to save the downloaded PDFs
SAVE_DIR = "./UNI/SEM10-MACHINE-LEARNING-PROJECT/summary_pdfs"
os.makedirs(SAVE_DIR, exist_ok=True)

# List to store all collected PDF links
pdf_links = []


def scrape_pdf_links():
    """
    Scrape the website to collect all PDF links from the 'Summary' column.
    """

    # Iterate through all pages (1 to 628)
    for page_num in range(3, 4):
        page_url = f"{BASE_URL}{page_num}"
        print(f"Processing: {page_url}")

        try:
            # Send a GET request to the page
            response = requests.get(page_url, verify=False)

            # Check if the page was successfully retrieved
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find the table containing the data using its ID
                table = soup.find('table', {'id': 'dataTable'})

                if table:
                    # Skip the header row and iterate through the data rows
                    rows = table.find_all('tr')[1:]

                    for row in rows:
                        columns = row.find_all('td')

                        # Ensure the 'Summary' column (6th column) exists
                        if len(columns) > 5:
                            summary_link = columns[5].find('a')

                            # If a 'Download' link exists, extract the PDF URL
                            if summary_link and 'href' in summary_link.attrs:
                                pdf_url = summary_link['href']

                                # Handle both relative and absolute URLs
                                full_url = pdf_url if pdf_url.startswith("http") else "https://misc.bpdb.gov.bd" + pdf_url
                                
                                # Add to the list of links
                                pdf_links.append(full_url)
                                print(f"Found PDF link: {full_url}")

            else:
                print(f"Failed to retrieve {page_url} - Status code: {response.status_code}")

        except Exception as e:
            print(f"Error processing page {page_num}: {e}")

    # Print collected links
    print("\nCollected PDF Links:")
    for link in pdf_links:
        print(link)

    print(f"\nTotal PDF links found: {len(pdf_links)}")


def download_file(url):
    """
    Download a single PDF file and save it locally.
    """

    # Extract the file name from the URL
    file_name = os.path.join(SAVE_DIR, url.split("/")[-1])

    try:
        # Request the file from the URL
        response = requests.get(url, stream=True, verify=False)

        # Check if the request was successful
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download: {url}, Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error downloading {url}: {e}")


def download_all_pdfs():
    """
    Loop through all collected PDF links and download them.
    """

    if not pdf_links:
        print("No PDF links found to download.")
        return

    for pdf_url in pdf_links:
        download_file(pdf_url)

    print("\nAll downloads completed.")


# Run the scraping and downloading processes
if __name__ == "__main__":
    print("Starting PDF link scraping...\n")
    scrape_pdf_links()
    print("\nStarting download process...\n")
    download_all_pdfs()