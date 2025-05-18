from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Set up Chrome WebDriver using webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the page
driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")

# Let the page load
time.sleep(2)

results = driver.find_elements(By.CLASS_NAME, "cp-search-result-item")

for item in results:
    title = item.find_element(By.CLASS_NAME, "title-content").text
    authors = [a.text for a in item.find_elements(By.CLASS_NAME, "author-link")]
    format_type = item.find_element(By.CLASS_NAME, "display-info-primary").text
    year = format_type.split("-")[1].strip()
    format = format_type.split("-")[0].strip()
    
    # print
    print(f"Title: {title}")
    print(f"Authors: {', '.join(authors)}")
    print(f"Format: {format}, Year: {year}")
    print("--------")


# Close the browser
driver.quit()


