import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from api.client import fetch_loopnet_data
    from parsing.parsers import parse_property_data
    from storage.mongo import save_to_mongo
    print("✅ All modules loaded successfully!")
except ImportError as e:
    print(f"❌ Module Import Error: {e}")
    print("Double check that your filenames are exactly: client.py, parsers.py, and mongo.py")

def run_pipeline():
    print("Starting Real Estate Market Monitor Pipeline...")

    raw_properties = fetch_loopnet_data(pages=3)
    
    if not raw_properties:
        print("No data fetched. Pipeline stopping.")
        return

    cleaned_properties = []
    for item in raw_properties:
        cleaned_item = parse_property_data(item)
        cleaned_properties.append(cleaned_item)
    
    print(f"Cleaned {len(cleaned_properties)} properties.")

    save_to_mongo(cleaned_properties, "loopnet_listings")

    print("Pipeline finished successfully!")

if __name__ == "__main__":
    run_pipeline()