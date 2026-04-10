import os
from pymongo import MongoClient
from dotenv import load_dotenv

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logging

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

def save_to_mongo(data_list, collection_name):
    """This function takes a list of houses and saves them to MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        db = client["RealEstateDB"]
        collection = db[collection_name]
        
        if data_list:
            result = collection.insert_many(data_list)
            logging.info(f"Success! Saved {len(result.inserted_ids)} houses to MongoDB.")
        else:
            logging.warning("No data to save.")
            
    except Exception as e:
        logging.error(f"MongoDB Error: {e}")

def save_image_metadata(metadata_list):
    """Saves property image metadata into a separate collection."""
    try:
        client = MongoClient(MONGO_URI)
        db = client["RealEstateDB"]
        collection = db["image_metadata"]
        
        if metadata_list:
            result = collection.insert_many(metadata_list)
            logging.info(f"Success! Saved {len(result.inserted_ids)} image metadata entries to MongoDB.")
        else:
            logging.warning("No image metadata to save.")
            
    except Exception as e:
        logging.error(f"MongoDB Metadata Error: {e}")
