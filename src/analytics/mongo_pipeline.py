from pymongo import MongoClient

def run_aggregation(mongo_uri, db_name, collection_name, pipeline):
    """
    Executes a MongoDB aggregation pipeline and returns the result as a list of dicts.
    """
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    return list(collection.aggregate(pipeline))
