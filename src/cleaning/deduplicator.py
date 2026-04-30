import pandas as pd
from utils.logger import logging

def remove_duplicates(df, key_columns=None):
    """
    Identifies and removes exact and key duplicates.
    """
    logging.info("--- Deduplication Process ---")
    
    # 1. Exact duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    logging.info(f"Removed {initial_len - len(df)} fully identical rows.")
    
    # 2. Key duplicates (e.g., listing_id)
    if key_columns is None:
        key_columns = ['listing_id']
    
    for col in key_columns:
        if col in df.columns:
            curr_len = len(df)
            df = df.drop_duplicates(subset=[col])
            logging.info(f"Dropped {curr_len - len(df)} repeated IDs based on: {col}")
            
    # 3. Subset duplicates (e.g., same title and date listed) - Requirement: "duplicate titles with same release date"
    if 'title' in df.columns and 'date_listed' in df.columns:
        curr_len = len(df)
        df = df.drop_duplicates(subset=['title', 'date_listed'])
        logging.info(f"Removed {curr_len - len(df)} duplicate titles with the same listing date.")
            
    return df

def count_duplicates_helper(df, column=None):
    """
    Helper function to count duplicates in a chosen column.
    """
    if column and column in df.columns:
        count = df.duplicated(subset=[column]).sum()
        logging.info(f"Duplicate count for column '{column}': {count}")
        return count
    count = df.duplicated().sum()
    logging.info(f"Total exact duplicate count: {count}")
    return count
