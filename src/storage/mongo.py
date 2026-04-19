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

# --- LAB 7 AUDIO/VIDEO EXTENSION ---
def save_transcript_to_mongo(transcript_data, source_path, language, model_metadata):
    """
    Saves a transcript document to MongoDB.
    Includes timestamps, language, model metadata, and original source path.
    """
    try:
        from datetime import datetime
        client = MongoClient(MONGO_URI)
        db = client["RealEstateDB"]
        collection = db["transcripts"]
        
        document = {
            "source_path": source_path,
            "language": language,
            "model_metadata": model_metadata,
            "transcript_text": transcript_data.get("text", ""),
            "segments": transcript_data.get("segments", []),
            "timestamp": datetime.now(),
            "status": "processed"
        }
        
        result = collection.insert_one(document)
        logging.info(f"Success! Saved transcript for {source_path} to MongoDB with ID {result.inserted_id}.")
        return result.inserted_id
            
    except Exception as e:
        logging.error(f"MongoDB Transcript Error: {e}")
        return None
