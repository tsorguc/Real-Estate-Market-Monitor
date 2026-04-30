import pandas as pd
import os
from utils.logger import logging
from cleaning.missing_handler import handle_missing_values, generate_missing_value_report
from cleaning.string_cleaner import clean_string_columns, normalize_property_types
from cleaning.deduplicator import remove_duplicates
from cleaning.type_converter import convert_types, get_memory_usage_report
from cleaning.validator import validate_data
from analytics.regex_ops import extended_regex_cleaning

def run_cleaning_pipeline(df):
    """
    Combines all cleaning steps into one reusable workflow.
    """
    logging.info("Starting Data Cleaning Pipeline...")
    
    # Create a copy to avoid modifying the original during processing steps if needed
    clean_df = df.copy()

    # 1. Missing Value Report
    generate_missing_value_report(clean_df)

    # 2. Handle Missing Values
    clean_df = handle_missing_values(clean_df)

    # 3. String Cleaning
    clean_df = clean_string_columns(clean_df)
    clean_df = normalize_property_types(clean_df)

    # 4. Regex Cleaning (Extended)
    clean_df = extended_regex_cleaning(clean_df)

    # 5. Deduplication
    clean_df = remove_duplicates(clean_df)

    # 6. Type Conversion
    clean_df = convert_types(clean_df)
    get_memory_usage_report(clean_df)

    # 7. Data Validation
    is_valid = validate_data(clean_df)
    if not is_valid:
        logging.warning("Cleaned data failed validation checks.")

    # 8. Save Cleaned Dataset
    output_dir = "data/processed/cleaned"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "cleaned_data.csv")
    clean_df.to_csv(output_path, index=False)
    logging.info(f"Cleaned dataset saved to {output_path}")

    logging.info("Data Cleaning Pipeline completed.")
    return clean_df
