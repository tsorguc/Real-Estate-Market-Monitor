import sys
import os

# Ensure Python finds your 'src' folders per lab instructions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import logging
from api.client import fetch_loopnet_data
from parsing.parsers import parse_loopnet_map_data
from storage.mongo import save_to_mongo
from storage.s3 import upload_file_to_s3

def run_pipeline():
    logging.info("Starting Real Estate Market Monitor Pipeline...")

    # 1. Fetch live data (Pages=3)
    logging.info("Fetching data from API...")
    raw_properties = fetch_loopnet_data(pages=3)

    if not raw_properties:
        logging.error("No data fetched from API. Pipeline stopping.")
        return

    # 2. Parse and Save to MongoDB
    logging.info("Parsing data...")
    cleaned_properties = [parse_loopnet_map_data(item) for item in raw_properties] # <-- Changed this
    
    logging.info("Saving to MongoDB...")
    save_to_mongo(cleaned_properties, "loopnet_listings")

    # 3. Upload raw pages to S3
    logging.info("Uploading raw files to S3...")
    for page in range(1, 4):
        file_name = f"loopnet_page_{page}.json"
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../../data/raw/api/{file_name}"))
        upload_file_to_s3(file_path, file_name)

    logging.info("Pipeline finished successfully")

if __name__ == "__main__":
    run_pipeline()