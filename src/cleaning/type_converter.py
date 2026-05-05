import pandas as pd
from utils.logger import logging

def convert_types(df):
    """
    Converts columns to appropriate data types.
    """
    logging.info("Converting data types...")
    
    # 1. Convert price and area to numeric
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce').astype('float32')
        logging.info("Converted 'price' to float32.")
        
    if 'area' in df.columns:
        df['area'] = pd.to_numeric(df['area'], errors='coerce').astype('float32')
        logging.info("Converted 'area' to float32.")

    # 2. Convert date_listed to datetime
    if 'date_listed' in df.columns:
        df['date_listed'] = pd.to_datetime(df['date_listed'], errors='coerce')
        logging.info("Converted 'date_listed' to datetime.")

    # 3. Convert low-cardinality strings to categories
    for col in ['type', 'status']:
        if col in df.columns:
            df[col] = df[col].astype('category')
            logging.info(f"Converted '{col}' to category.")

    # 4. Convert listing_id or numeric IDs to Int64 (nullable)
    if 'listing_id_numeric' in df.columns: # Assuming some numeric ID
        df['listing_id_numeric'] = pd.to_numeric(df['listing_id_numeric'], errors='coerce').astype('Int64')
        logging.info("Converted 'listing_id_numeric' to Int64.")

    return df

def get_memory_usage_report(df):
    """
    Returns a report of memory usage per column.
    """
    memory_usage = df.memory_usage(deep=True)
    total_memory = memory_usage.sum() / 1024**2
    logging.info(f"Total memory usage: {total_memory:.2f} MB")
    return memory_usage
