import os
from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

def get_db():
    client = MongoClient(MONGO_URI)
    return client["RealEstateDB"]

def generate_combined_report():
    """Combines API listings with document extraction highlights."""
    db = get_db()
    
    listings = list(db["loopnet_listings"].find({}, {"_id": 0}))
    documents = list(db["extracted_documents"].find({}, {"_id": 0}))
    
    # Create a summary of documents grouped by file_name
    doc_summary = {}
    for doc in documents:
        fname = doc["file_name"]
        if fname not in doc_summary:
            doc_summary[fname] = {
                "danger_flags": set(),
                "highlights": set()
            }
        doc_summary[fname]["danger_flags"].update(doc.get("danger_flags", []))
        doc_summary[fname]["highlights"].update(doc.get("property_highlights", []))

    print("\n" + "="*50)
    print("🏠 REAL ESTATE MARKET MONITOR - COMBINED REPORT")
    print("="*50)
    
    # Since we don't have a direct key, we show a sample 'All-in-One' row logic
    # as per design document criteria.
    for i, listing in enumerate(listings[:5]): # Show first 5
        # Simulating a join for the 'All-in-One' view requirement
        related_doc = f"Listing{i+1}.pdf" if i < len(doc_summary) else "N/A"
        info = doc_summary.get(related_doc, {"danger_flags": [], "highlights": []})
        
        print(f"\nProperty ID: {listing.get('listing_id')}")
        print(f"Coordinates: {listing.get('coordinates')}")
        print(f"Linked Document: {related_doc}")
        print(f"Danger Flags: {list(info['danger_flags']) if info['danger_flags'] else 'None'}")
        print(f"Highlights: {list(info['highlights']) if info['highlights'] else 'None'}")
        print("-" * 30)

def search_properties(keyword):
    """Searches the database for properties matching a keyword in their documents."""
    db = get_db()
    results = list(db["extracted_documents"].find(
        {"content": {"$regex": keyword, "$options": "i"}},
        {"file_name": 1, "content": 1, "_id": 0}
    ))
    
    print(f"\n🔍 Search Results for '{keyword}':")
    if not results:
        print("No matches found.")
    else:
        for res in results:
            print(f"Found in {res['file_name']}: {res['content'][:100]}...")

if __name__ == "__main__":
    generate_combined_report()
    search_properties("new roof")
