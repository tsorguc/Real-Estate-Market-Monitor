from io_utils import read_json, setup_logging

if __name__ == "__main__":
    setup_logging("pipeline.log")
    
    json_path = "data/raw/real_estate/loopNet-sample.json"
    
    real_estate_data = read_json(json_path)
    
    if real_estate_data:
        print("--- LoopNet Data Loaded Successfully ---")
    else:
        print("Failed to load data. Check pipeline.log for details.")