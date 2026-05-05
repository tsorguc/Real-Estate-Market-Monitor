import pandas as pd
from utils.logger import logging

def validate_data(df):
    """
    Performs logical checks and assertions to confirm data quality.
    Utilizes Python's built-in assert statements.
    """
    logging.info("--- Data Validation Phase ---")
    
    try:
        # 1. Check for nulls in critical columns
        if 'listing_id' in df.columns:
            assert df['listing_id'].notnull().all(), "Validation Error: Found null listing_ids!"
            
        # 2. Check price ranges
        if 'price' in df.columns:
            assert (df['price'] > 0).all(), "Validation Error: Found non-positive prices!"
            
        # 3. Check area ranges
        if 'area' in df.columns:
            assert (df['area'] > 0).all(), "Validation Error: Found non-positive areas!"

        # 4. Check for duplicates in listing_id
        if 'listing_id' in df.columns:
             assert not df['listing_id'].duplicated().any(), "Validation Error: Duplicate listing_ids found!"

        # 5. Domain Specific: Check Property Types
        if 'type' in df.columns:
            allowed_types = ['Office', 'Retail', 'Industrial', 'Multi-Family', 'Commercial', 'Unknown']
            # Cast to string for set comparison
            found_types = set(df['type'].astype(str).unique())
            # We don't fail here if new types found but we log it
            logging.info(f"Unique property types found: {found_types}")

        # 6. Domain Specific: Date check (not before 1800, equivalent to movie release year check)
        if 'date_listed' in df.columns:
            # Check if dates are within reasonable range if they are datetime
            if pd.api.types.is_datetime64_any_dtype(df['date_listed']):
                assert df['date_listed'].dt.year.min() >= 1800, "Validation Error: Listing year before 1800 found!"

        logging.info("Cleaned data successfully meets all expectations.")
        return True
    except AssertionError as e:
        logging.error(f"Failing fast: {e}")
        return False
