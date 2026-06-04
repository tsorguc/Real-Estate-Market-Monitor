import os
import sys
import pandas as pd
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils.logger import logging

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "RealEstateDB"
COLLECTION_NAME = "loopnet_listings"
CSV_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "cleaned", "cleaned_data.csv")

def seed_database():
    """
    Reads cleaned CSV, connects to MongoDB, drops existing collection,
    inserts records, and creates indexes.
    """
    logging.info("Starting MongoDB seeding process...")
    print("Seeding MongoDB...")
    
    # 1. Check if cleaned CSV exists
    if not os.path.exists(CSV_PATH):
        error_msg = f"Cleaned CSV file not found at: {CSV_PATH}. Make sure to run the cleaning pipeline first."
        logging.error(error_msg)
        print(f"ERROR: {error_msg}")
        sys.exit(1)
        
    # 2. Read CSV
    try:
        df = pd.read_csv(CSV_PATH)
        logging.info(f"Loaded {len(df)} records from CSV.")
    except Exception as e:
        logging.error(f"Failed to read CSV: {e}")
        print(f"ERROR: Failed to read CSV: {e}")
        sys.exit(1)
        
    # 3. Connect to MongoDB
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.server_info()  # Force connection check
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Drop existing collection to reseed clean
        logging.info(f"Dropping collection {COLLECTION_NAME} if it exists...")
        collection.drop()
        
        # 4. Prepare records to insert
        records = df.to_dict(orient="records")
        
        # Add year column explicitly for indexing/filtering
        for record in records:
            if 'collected_at' in record and pd.notna(record['collected_at']):
                try:
                    record['year'] = int(pd.to_datetime(record['collected_at']).year)
                except Exception:
                    record['year'] = 2026
            else:
                record['year'] = 2026
                
            # Handle float conversions for mongo compatibility (avoid nan issues)
            for k, v in record.items():
                if pd.isna(v):
                    record[k] = None
        
        # 5. Insert records
        if records:
            result = collection.insert_many(records)
            logging.info(f"Inserted {len(result.inserted_ids)} records into MongoDB.")
            print(f"Seeding Complete: Inserted {len(result.inserted_ids)} records.")
        else:
            logging.warning("No records to insert.")
            print("Warning: No records to insert.")
            
        # 6. Create indexes for type (genre), year, and title
        logging.info("Creating indexes for type, year, and title...")
        collection.create_index([("type", ASCENDING)])
        collection.create_index([("year", ASCENDING)])
        collection.create_index([("title", ASCENDING)])
        logging.info("Indexes created successfully.")
        print("Indexes created on 'type', 'year', and 'title'.")
        
    except Exception as e:
        logging.error(f"MongoDB seeding failed: {e}")
        print(f"ERROR: Seeding failed: {e}")
        print("WARNING: MongoDB seeding failed. The dashboard will fall back to local CSV data.")
        return

if __name__ == "__main__":
    seed_database()
