from datetime import datetime

def parse_property_data(raw_item):
    """Takes a messy LoopNet house and picks only the good parts."""
    return {
        "property_id": raw_item.get("propertyId"),
        "name": raw_item.get("propertyName"),
        "address": raw_item.get("address"),
        "price": raw_item.get("price"),
        "sq_ft": raw_item.get("squareFeet"),
        "collected_at": datetime.now().isoformat(), # This is your Timestamp metadata!
        "source": "LoopNet API"
    }