import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("LOOPNET_API_KEY")

def fetch_loopnet_data(pages=3):
    all_results = []
    # This is the most reliable endpoint for 'Sale' listings
    url = "https://loopnet-api.p.rapidapi.com/loopnet/sale/searchByCity"
    
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "loopnet-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    for page in range(1, pages + 1):
        print(f"--- Fetching Page {page} ---")
        
        # We'll use 'location' and 'pageIndex' - the gold standard for this API
        payload = {
            "location": "NY", # Try a short state code first
            "pageIndex": page
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status() 
            
            data = response.json()
            
            # LoopNet often nests items inside 'searchResult' or 'items'
            # This check looks in both places just in case!
            items = data.get('items') or data.get('searchResult', {}).get('items', [])
            
            if not items:
                print(f"⚠️ Page {page} returned no houses. Trying different payload...")
                # Backup attempt with 'city' instead of 'location'
                payload = {"city": "New York", "pageIndex": page}
                response = requests.post(url, json=payload, headers=headers)
                items = response.json().get('items', [])

            all_results.extend(items)
            print(f"Successfully grabbed {len(items)} items from page {page}")
            
        except Exception as e:
            print(f"❌ API Error: {e}")
            break
            
    return all_results

if __name__ == "__main__":
    results = fetch_loopnet_data(3)
    print(f"✅ Success! Grabbed {len(results)} properties total.")