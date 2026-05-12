from src.utils.logger import logging

def demonstrate_selection(df):
    """
    Demonstrates pandas selection and filtering techniques.
    As per Lab 8 Requirements.
    """
    logging.info("--- Data Selection & Filtering ---")
    
    # 1. loc and iloc
    # Select first 5 rows and specific columns using loc
    if 'listing_id' in df.columns and 'price' in df.columns:
        subset_loc = df.loc[:4, ['listing_id', 'price']]
        logging.info(f"loc selection (first 5 rows, listing_id & price):\n{subset_loc}")
    
    # Select first 3 rows and first 2 columns using iloc
    subset_iloc = df.iloc[:3, :2]
    logging.info(f"iloc selection (first 3 rows, first 2 columns):\n{subset_iloc}")
    
    # 2. Boolean Filtering
    if 'price' in df.columns:
        high_value = df[df['price'] > 1000000]
        logging.info(f"High value properties (price > 1M): {len(high_value)} found.")
        
    # 3. isin and between
    if 'type' in df.columns:
        target_types = ['Office', 'Retail']
        filtered_types = df[df['type'].isin(target_types)]
        logging.info(f"Properties with type in {target_types}: {len(filtered_types)} found.")
        
    if 'price' in df.columns:
        mid_range = df[df['price'].between(500000, 1000000)]
        logging.info(f"Mid-range properties (500k-1M): {len(mid_range)} found.")
        
    return "Selection demonstration completed."
