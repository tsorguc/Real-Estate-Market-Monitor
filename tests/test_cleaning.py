import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path to import cleaning modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cleaning.missing_handler import handle_missing_values
from cleaning.string_cleaner import clean_string_columns
from cleaning.deduplicator import remove_duplicates, count_duplicates_helper
from cleaning.type_converter import convert_types
from cleaning.validator import validate_data

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'listing_id': ['L1', 'L2', 'L1', 'L3', 'L4', None],
        'price': [100000, 0, 100000, 200000, 500000, 300000],
        'area': [1000, 2000, 1000, 1500, np.nan, 2500],
        'description': ['Nice office ', 'Retail space', 'Nice office ', None, 'Big warehouse', 'Unknown'],
        'type': ['office', 'RETAIL', 'office', 'office', 'industrial', 'office'],
        'date_listed': ['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-04', 'invalid-date', '2023-01-05'],
        'title': ['T1', 'T2', 'T1', 'T3', 'T4', 'T5']
    })

def test_drop_rows_missing_listing_id(sample_df):
    cleaned_df = handle_missing_values(sample_df, critical_columns=['listing_id'])
    assert cleaned_df['listing_id'].isnull().sum() == 0
    assert len(cleaned_df) == 5

def test_replace_zero_price_with_median(sample_df):
    # Before median fill, zeros are replaced with NaN
    cleaned_df = handle_missing_values(sample_df, numeric_columns=['price'])
    # Remaining prices (after drop None ID and zero replace): [100000, 100000, 200000, 500000]
    # Median is 150000
    assert 0 not in cleaned_df['price'].values
    assert cleaned_df.loc[sample_df['listing_id'] == 'L2', 'price'].iloc[0] == 150000

def test_fill_missing_description(sample_df):
    cleaned_df = handle_missing_values(sample_df, text_columns=['description'])
    assert cleaned_df['description'].isnull().sum() == 0
    assert "No description provided" in cleaned_df['description'].values

def test_clean_string_columns(sample_df):
    cleaned_df = clean_string_columns(sample_df, columns=['description', 'type'])
    assert cleaned_df['description'].iloc[0] == 'nice office'
    assert cleaned_df['type'].iloc[1] == 'retail'

def test_remove_exact_duplicates(sample_df):
    # Row 2 is exactly like Row 0
    assert count_duplicates_helper(sample_df) == 1
    cleaned_df = remove_duplicates(sample_df)
    assert len(cleaned_df) == 5

def test_convert_types(sample_df):
    # Need to handle nulls/zeros first
    df = handle_missing_values(sample_df)
    df = convert_types(df)
    assert df['price'].dtype == 'float32'
    assert df['type'].dtype == 'category'
    assert pd.api.types.is_datetime64_any_dtype(df['date_listed'])

def test_validate_data_passes(sample_df):
    # Clean the data first
    df = handle_missing_values(sample_df)
    df = remove_duplicates(df)
    df = convert_types(df)
    # Ensure all prices > 0 and year >= 1800 for validation
    df['price'] = df['price'].replace(0, 100000)
    # Fix invalid date for datetime conversion if needed
    df.loc[df['listing_id'] == 'L4', 'date_listed'] = pd.to_datetime('2023-01-01')
    assert validate_data(df) is True

def test_validate_data_fails_on_null_id():
    df = pd.DataFrame({'listing_id': [None, 'L2'], 'price': [100, 200], 'area': [10, 20]})
    assert validate_data(df) is False
