import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from urllib.parse import urlparse
import time

def extract_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        with requests.get(url, headers=headers) as response:
            response.raise_for_status()
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                for tag in ['head','header', 'footer','foot,''navigation','nav','dropdown']:
                    elements_to_remove = soup.find_all(tag)
                    for elem in elements_to_remove:
                        elem.decompose()
                # Extract text from the remaining elements
                text_content = ' '.join(soup.stripped_strings)
                # remove extra spaces and line breaks
                text_content = re.sub(r"\s+", " ", text_content).strip()
                # add spaces between words that are capitalized
                text_content = re.sub(r'(?<!^)(?=[A-Z])', ' ', text_content)
                # remove punctuation
                words = text_content.split()
                # remove single word characters because of middle initials
                filtered_words = [word for word in words if len(word) > 1]
                filtered_text = ' '.join(filtered_words)
                return filtered_text
            
            except Exception as e:
                print(f"An error occurred while parsing HTML for URL {url}: {e}")
                return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing URL {url}: {e}")
        return None

def process_links(links):
    results = []
    max_threads = 10
    delay = 1 # seconds
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures_to_link = {executor.submit(extract_content, link): link for link in links}
        for future in as_completed(futures_to_link):
            link = futures_to_link[future]
            try:
                extracted_content = future.result()
                results.append((link, extracted_content))
            except Exception as e:
                print(f"An error occurred while processing URL {link}: {e}")
            time.sleep(delay) # time sleep to avoid being blacklisted
    return results

