import os
import requests
import json
from dotenv import load_dotenv

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logging

load_dotenv()
API_KEY = os.getenv("LOOPNET_API_KEY")

def fetch_loopnet_data(pages=3):
    all_results = []
    url = "https://loopnet-api.p.rapidapi.com/loopnet/sale/searchByCity"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "loopnet-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    # Ensure the directory required by the lab exists
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    api_raw_dir = os.path.join(project_root, "data", "raw", "api")
    os.makedirs(api_raw_dir, exist_ok=True)

    for page in range(1, pages + 1):
        logging.info(f"--- Fetching Page {page} ---")
        payload = {"cityId": "11854", "page": page}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status() 
            
            data = response.json()
            items = data.get('data') or data.get('searchResult', {}).get('items', [])
            
            if not items:
                logging.warning(f"Page {page} returned no houses. Trying backup payload...")
                payload = {"city": "New York", "pageIndex": page}
                response = requests.post(url, json=payload, headers=headers)
                items = response.json().get('items', [])

            all_results.extend(items)
            logging.info(f"Successfully grabbed {len(items)} items from page {page}")
            
            # LAB REQUIREMENT: Save raw data from each page individually
            page_file = os.path.join(api_raw_dir, f"loopnet_page_{page}.json")
            with open(page_file, "w", encoding="utf-8") as f:
                json.dump(items, f)
            logging.info(f"Saved raw data to {page_file}")
            
        except Exception as e:
            logging.error(f"API Error: {e}")
            break
            
    return all_results

if __name__ == "__main__":
    fetch_loopnet_data(3)