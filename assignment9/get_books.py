from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
import json

# Set up Chrome WebDriver using webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the page
driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")

# Let the page load
time.sleep(2)

LI_CLASS_NAME = "cp-search-result-item"             # the <li> class for each result
TITLE_CLASS = "title-content"                       # the <span> class for the title result
AUTHOR_CLASS = "author-link"                        # the <span> class for each author link
FORMAT_YEAR_CLASS = "display-info-primary"          # the <span> class that contains format/year


# Find all list item search results
search_results = driver.find_elements(By.TAG_NAME, "li")
results = []

for item in search_results:
    try:
        # Title
        title_element = item.find_element(By.CLASS_NAME, TITLE_CLASS)
        title = title_element.text.strip()

        # Authors 
        author_elements = item.find_elements(By.CLASS_NAME, AUTHOR_CLASS)
        authors = "; ".join([a.text.strip() for a in author_elements])

        # Format and Year
        format_type = item.find_element(By.CLASS_NAME, FORMAT_YEAR_CLASS).text
        year = format_type.split("-")[1].strip()
        format = format_type.split("-")[0].strip()

        # Save into dictionary
        book_data = {
            "Title": title,
            "Author": authors,
            "Format": format,
            "year" : year
        }

        results.append(book_data)

    except Exception as e:
        # Skip any problematic entries
        print(f"Skipping one entry due to error: {e}")


driver.quit()

# Create DataFrame and print
df = pd.DataFrame(results)
print(df)

# Write DataFrame to CSV
csv_file_path = './assignment9/get_books.csv'
df.to_csv(csv_file_path, index=False)

# Optionally save to JSON
json_file_path = 'assignment9/get_books.json'
with open(json_file_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"Data saved to {csv_file_path} and {json_file_path}")
