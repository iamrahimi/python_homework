import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    driver.get(url)
    time.sleep(3)

    # Get page title
    title = driver.title

    data_rows = []

    # Add title row
    data_rows.append(['title', title, ''])

    # Get headers (h1 to h6)
    for level in range(1, 7):
        elements = driver.find_elements(By.TAG_NAME, f'h{level}')
        for elem in elements:
            text = elem.text.strip()
            if text:
                data_rows.append(['header', text, f'h{level}'])

    # Get up to 10 links
    links_collected = 0
    a_tags = driver.find_elements(By.TAG_NAME, 'a')
    for a in a_tags:
        href = a.get_attribute('href')
        text = a.text.strip()
        if text and href and href.startswith("https://en.wikipedia.org/wiki/"):
            data_rows.append(['link', text, href])
            links_collected += 1
            if links_collected == 10:
                break

    # Get images (src and alt)
    img_tags = driver.find_elements(By.TAG_NAME, 'img')
    for img in img_tags:
        src = img.get_attribute('src')
        alt = img.get_attribute('alt') or ''
        if src:
            data_rows.append(['image', alt, src])

    # Write to CSV
    csv_path = os.path.join('assignment10', 'page.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Header row
        writer.writerow(['type', 'content', 'extra'])
        writer.writerows(data_rows)

    print(f"Data saved to {csv_path}")

finally:
    driver.quit()