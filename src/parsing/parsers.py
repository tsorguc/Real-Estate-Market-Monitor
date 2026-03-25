import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import logging

def parse_loopnet_map_data(raw_item):
    """Extracts the listing ID and map coordinates from the LoopNet API response."""
    return {
        "listing_id": raw_item.get("listingId"),
        "coordinates": raw_item.get("coordinations", []),
        "collected_at": datetime.now().isoformat(),
        "source": "LoopNet API"
    }

def parse_json_files(file_path):
    """1. JSON Parsing Requirement"""
    logging.info(f"Parsing JSON file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Since your fetched data is a direct list (array) of dictionaries:
            items = data if isinstance(data, list) else data.get('data', [])
            
            return [parse_loopnet_map_data(item) for item in items]
    except Exception as e:
        logging.error(f"Error parsing JSON: {e}")
        return []

def parse_csv_file(file_path):
    """2. CSV Parsing Requirement"""
    logging.info(f"Parsing CSV file: {file_path}")
    parsed_data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                parsed_data.append(row)
        return parsed_data
    except FileNotFoundError:
        logging.error(f"CSV file not found: {file_path}")
        return []

def parse_xml_file(file_path):
    """3. XML Parsing Requirement"""
    logging.info(f"Parsing XML file: {file_path}")
    parsed_data = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for child in root:
            parsed_data.append({child.tag: child.text})
        return parsed_data
    except FileNotFoundError:
        logging.error(f"XML file not found: {file_path}")
        return []

if __name__ == "__main__":
    # Test block
    parse_json_files("../../data/raw/api/loopnet_page_1.json")
    parse_csv_file("../../data/raw/csv/sample.csv")
    parse_xml_file("../../data/raw/xml/sample.xml")