import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def discover_links(base_url):
    discovered_urls = set()
    urls_to_visit = {base_url}
    domain_name = urlparse(base_url).netloc
    excluded_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.php'}

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        parsed_url = urlparse(current_url)
        current_url = urlunparse(parsed_url._replace(fragment=""))
        if current_url in discovered_urls:
            continue

        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            discovered_urls.add(current_url)

            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(current_url, link['href'])
                parsed_absolute_link = urlparse(absolute_link)
                cleaned_link = urlunparse(parsed_absolute_link._replace(fragment=""))

                if not parsed_absolute_link.path.lower().endswith(tuple(excluded_extensions)) and urlparse(cleaned_link).netloc == domain_name:
                    urls_to_visit.add(cleaned_link)
        except Exception as e:
            continue

    return discovered_urls

def get_dynamic_content(url, driver):
    driver.get(url)
    time.sleep(5)
    return driver.page_source

def save_content(url, content):
    domain_name = urlparse(url).netloc
    filename = f"content/{domain_name}_{urlparse(url).path.replace('/', '_')}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def scrape_urls(urls, driver):
    for url in urls:
        try:
            content = get_dynamic_content(url, driver)
            save_content(url, BeautifulSoup(content, 'html.parser').get_text(separator='\n', strip=True))
        except Exception as e:
            continue
