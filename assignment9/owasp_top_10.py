import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Optional: If you want to use Chrome options
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Optional: run browser in background
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Correct instantiation with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get('https://owasp.org/www-project-top-ten/')
time.sleep(3)  

vulnerabilities = []

xpath = "//ul/li/a[contains(@href, 'https://owasp.org/Top10')]"

elements = driver.find_elements(By.XPATH, xpath)

for element in elements:
    vulnerability = {
        'title': element.text,
        'link': element.get_attribute('href')
    }
    vulnerabilities.append(vulnerability)


print(vulnerabilities)

# Save the data to owasp_top_10.csv
with open('assignment9/owasp_top_10.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'link'])
    writer.writeheader()
    writer.writerows(vulnerabilities)


driver.quit()