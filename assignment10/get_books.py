from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import json
import time

# Set up Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Load the webpage
driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")

# Give the page time to load
time.sleep(2)

# Class names (from task 2)
LI_CLASS_NAME = "cp-search-result-item"
TITLE_CLASS = "title-content"
AUTHOR_CLASS = "author-link"
FORMAT_YEAR_CLASS = "display-info-primary"

# Find all li elements for search results
search_results = driver.find_elements(By.CLASS_NAME, LI_CLASS_NAME)

# Create empty list to store results
results = []

# Loop through each result
for item in search_results:
    try:
        # Title
        title_element = item.find_element(By.CLASS_NAME, TITLE_CLASS)
        title = title_element.text.strip()

        # Authors
        author_elements = item.find_elements(By.CLASS_NAME, AUTHOR_CLASS)
        authors = "; ".join([a.text.strip() for a in author_elements])

        # Format-Year
        format_year_element = item.find_element(By.CLASS_NAME, FORMAT_YEAR_CLASS)
        format_year = format_year_element.text.strip()

        # Create dict for this book
        book_data = {
            "Title": title,
            "Author": authors,
            "Format-Year": format_year
        }

        # Append to results list
        results.append(book_data)

    except Exception as e:
        print(f"Skipping one entry due to error: {e}")

# Close the browser
driver.quit()

driver.quit()

# Create DataFrame and print
df = pd.DataFrame(results)
print(df)

# Write DataFrame to CSV
csv_file_path = './assignment10/get_books.csv'
df.to_csv(csv_file_path, index=False)

# Optionally save to JSON
json_file_path = 'assignment10/get_books.json'
with open(json_file_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"Data saved to {csv_file_path} and {json_file_path}")