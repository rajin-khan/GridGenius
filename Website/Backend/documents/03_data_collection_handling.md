# Data Collection and Handling in GridGenius

**Data Scarcity:** Obtaining comprehensive energy data for Bangladesh presented challenges due to data scarcity and website design.

**Data Source:**
*   The primary data source was the **Bangladesh Power Development Board (BPDB) website** (specifically the `misc.bpdb.gov.bd/daily-generation-archive` section).
*   Data was contained within **1800+ PDF reports**.

**Collection Process:**
1.  A **web scraper** (Python script using libraries like `requests` and `BeautifulSoup`) was developed to automatically navigate the BPDB archive pages and download all relevant PDF summary reports.
2.  Relevant data points (like peak generation, demand, date) were **extracted** from these PDFs using Python libraries (e.g., `PyPDF2` or `pdfplumber`).
3.  The extracted data was compiled into a structured format, specifically a **pandas DataFrame**, and saved as a CSV file.

**Data Cleaning & Anomaly Handling:**
*   **Missing Values:** An initial check using `isnull().sum()` confirmed **no missing values** in the collected dataset.
*   **Duplicated Values:**
    *   An initial check using `df.duplicated().any()` reported `False`.
    *   However, plotting the distribution of records over time revealed several dates with more than one entry.
    *   These specific **repeated date records were manually identified and dropped** from the dataset to ensure data integrity. Specific indices dropped included [1, 11, 13, 703, 705, 708, 855, 1072].
*   **Outlier Removal (for Modeling):**
    *   Outliers were detected using **Inter-Quartile Range (IQR)** and **Z-Score** methods.
    *   IQR method did not detect significant outliers in the primary features.
    *   Z-Score method successfully identified and flagged outliers, particularly in **Temperature** and **Generation** features.
    *   Outliers identified by Z-Score were handled (e.g., replaced with a rolling mean or removed) to create cleaned dataset variations (`energy_iter13b`, `energy_iter13d`) for model training. This resulted in 4 dataset variations combining different scaling and outlier removal techniques.