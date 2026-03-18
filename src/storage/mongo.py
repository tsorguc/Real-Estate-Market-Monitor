import os
from pymongo import MongoClient
from dotenv import load_dotenv

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
            print(f"Success! Saved {len(result.inserted_ids)} houses to MongoDB.")
        else:
            print("No data to save.")
            
    except Exception as e:
        print(f"MongoDB Error: {e}")