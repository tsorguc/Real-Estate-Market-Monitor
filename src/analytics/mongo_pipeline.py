import pandas as pd
from pymongo import MongoClient

def get_mongo_genre_stats(mongo_uri, db_name, collection_name):
    """
    Executes a 4-stage MongoDB aggregation pipeline and returns a DataFrame.
    Stages: $match, $group, $sort, $project as per Lab 10.
    """
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    
    pipeline = [
        # Stage 1: Filter (Match only listings with a price)
        {"$match": {"price": {"$gt": 0}}},
        
        # Stage 2: Group by property type (genre) and calculate stats
        {"$group": {
            "_id": "$type",
            "count": {"$sum": 1},
            "avg_price": {"$avg": "$price"}
        }},
        
        # Stage 3: Sort by count descending
        {"$sort": {"count": -1}},
        
        # Stage 4: Project to rename fields for readability
        {"$project": {
            "property_type": "$_id",
            "total_listings": "$count",
            "average_market_price": "$avg_price",
            "_id": 0
        }}
    ]
    
    results = list(collection.aggregate(pipeline))
    return pd.DataFrame(results)
