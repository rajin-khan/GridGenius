import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta

# ==== CONFIGURATION ====
chrome_path = r"G:\cc\chromedriver-win64\chromedriver.exe"  # Your ChromeDriver path
service = Service(executable_path=chrome_path)
driver = webdriver.Chrome(service=service)

url = "https://misc.bpdb.gov.bd/area-wise-demand"
start_date = datetime(2025, 1, 1)         # Start date
end_date = datetime(2025, 6, 10)         # End date (change as needed)

results = []

date = start_date
while date <= end_date:
    driver.get(url)
    time.sleep(2)  # Wait for page to load

    # Set the date in the input field
    date_input = driver.find_element(By.XPATH, '//input[@type="text"]')
    driver.execute_script("arguments[0].removeAttribute('readonly')", date_input)
    date_input.clear()
    date_input.send_keys(date.strftime('%d-%m-%Y'))
    time.sleep(1)

    # Click the Search button
    search_btn = driver.find_element(By.XPATH, '//button[contains(text(), "Search")]')
    search_btn.click()
    time.sleep(4)  # Wait for table to update

    try:
        tables = driver.find_elements(By.TAG_NAME, 'table')
        if len(tables) > 1:
            table = tables[1]
            rows = table.find_elements(By.TAG_NAME, 'tr')
            count = 0
            for row in rows[1:-1]:  # Skip header and "Total" row
                cols = row.find_elements(By.TAG_NAME, 'td')
                if len(cols) == 4:
                    results.append({
                        'Date': date.strftime('%Y-%m-%d'),
                        'Zone': cols[1].text.strip(),
                        'Demand (MW)': cols[2].text.strip(),
                        'Load Shed (MW)': cols[3].text.strip()
                    })
                    count += 1
            print(f"Scraped date: {date.strftime('%Y-%m-%d')} ({count} rows)")
        else:
            print(f"Table not found for date {date.strftime('%Y-%m-%d')}")
    except Exception as e:
        print(f"Error on date {date.strftime('%Y-%m-%d')}: {e}")

    # Random sleep to avoid rate-limiting/blocking
    time.sleep(random.uniform(2, 5))
    date += timedelta(days=1)

driver.quit()

print("Collected data preview:")
for row in results[:10]:
    print(row)
print(f"Total rows collected: {len(results)}")

# === Save as CSV ===
df = pd.DataFrame(results)
df.to_csv('bpdb_area_demand_full_2.csv', index=False)
print("Done! Data saved to bpdb_area_demand_full.csv")
