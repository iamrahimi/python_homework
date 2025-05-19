from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    driver.get(url)

    # Wait for page to load (simple wait, can be improved with explicit waits)
    time.sleep(3)

    # Extract the title
    title = driver.title

    # Extract headers (h1, h2, h3, h4, h5, h6)
    headers = []
    for level in range(1, 7):
        elements = driver.find_elements(By.TAG_NAME, f'h{level}')
        for elem in elements:
            text = elem.text.strip()
            if text:
                headers.append(text)

    # Extract links (filter for internal wiki links)
    links = []
    a_tags = driver.find_elements(By.TAG_NAME, 'a')
    for a in a_tags:
        href = a.get_attribute('href')
        text = a.text.strip()
        if text and href and href.startswith("https://en.wikipedia.org/wiki/"):
            links.append({'text': text, 'href': href})
            if len(links) == 10:
                break

    # Prepare data dictionary
    data = {
        'title': title,
        'headers': headers,
        'links': links
    }

    # Write to page.json
    with open('assignment10/page.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Data saved to page.json successfully.")

finally:
    driver.quit()