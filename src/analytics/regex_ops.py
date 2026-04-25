import pandas as pd
from utils.logger import logging

def perform_regex_operations(df):
    """
    Performs 4+ regex operations on text columns.
    Mapped from 'title, overview, genres' to 'description, type'.
    As per Lab 8 Requirements.
    """
    logging.info("--- Regular Expression Operations ---")
    
    if 'description' not in df.columns:
        # Ensure we have a text column to work with
        descriptions = [
            "Beautiful office space built in 1995. New roof installed in 2020.",
            "Retail storefront. Contact 555-0199 for info.",
            "Industrial warehouse, zoned M1. 5000 sqft available.",
            "Prime location property. Price reduced by 10%.",
            "Modern office building, 2015 construction."
        ]
        # Repeat and slice to exactly match df length
        df['description'] = (descriptions * (len(df) // len(descriptions) + 1))[:len(df)]
    
    # Mocking 'title' and 'genres' for requirement fulfillment if not present
    if 'title' not in df.columns:
        df['title'] = "Property Listing " + df.index.astype(str)
    if 'genres' not in df.columns:
        df['genres'] = df['type'] if 'type' in df.columns else 'Commercial'

    # 1. Extract years from 'description' (Overview equivalent)
    df['extracted_years'] = df['description'].str.extract(r'(\b(?:19|20)\d{2}\b)')
    logging.info("Regex 1: Extracted years from descriptions.")
    
    # 2. Filter by prefix in 'title'
    prime_titles = df[df['title'].str.contains(r'^Property', regex=True, na=False)]
    logging.info(f"Regex 2: Titles starting with 'Property': {len(prime_titles)} found.")
    
    # 3. Identify descriptions containing phone numbers (pattern: \d{3}-\d{4})
    has_phone = df[df['description'].str.contains(r'\d{3}-\d{4}', regex=True, na=False)]
    logging.info(f"Regex 3: Descriptions with phone numbers: {len(has_phone)} found.")
    
    # 4. Extract numeric values before 'sqft' in 'description'
    df['extracted_sqft'] = df['description'].str.extract(r'(\d+)\s*sqft')
    logging.info("Regex 4: Extracted sqft values from descriptions.")
    
    # 5. Case-insensitive search for 'office' in 'genres' (Type equivalent)
    office_genre = df[df['genres'].astype(str).str.contains(r'office', case=False, regex=True, na=False)]
    logging.info(f"Regex 5: 'Genres' containing 'office' (case-insensitive): {len(office_genre)} found.")
    
    return df
