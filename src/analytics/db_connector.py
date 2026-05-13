import pymysql
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables (assuming DB credentials are in .env)
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "real_estate_db")

def get_connection():
    """Creates and returns a connection to the MySQL database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def populate_financials(csv_path):
    """
    Reads the cleaned dataset and populates the 'property_financials' table.
    """
    df = pd.read_csv(csv_path)
    
    # Map real estate columns to consistent names for analytics
    # Expected columns in cleaned_data.csv: price, collected_at, listing_id, area, type, title
    mapping = {
        'listing_id': 'listing_id',
        'title': 'title',
        'price': 'price',
        'area': 'area',
        'type': 'property_type'
    }
    
    # Ensure columns exist, if not, create them or handle them
    for target in mapping.keys():
        if target not in df.columns:
            if target == 'title': df['title'] = "Unknown Property"
            elif target == 'price': df['price'] = 0
            elif target == 'area': df['area'] = 0
            elif target == 'type': df['type'] = 'Commercial'

    # Extract year from collected_at for trend analysis
    if 'collected_at' in df.columns:
        df['year'] = pd.to_datetime(df['collected_at']).dt.year
    else:
        df['year'] = datetime.now().year

    required_columns = ['listing_id', 'title', 'price', 'area', 'year', 'type']
    # Filter only available columns from the required list to avoid crashes
    cols_to_use = [c for c in required_columns if c in df.columns]
    df_to_save = df[cols_to_use].dropna()
    
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
    df_to_save.to_sql('property_financials', con=engine, if_exists='replace', index=False)
    print(f"Successfully populated 'property_financials' table with {len(df_to_save)} records.")

def query_financials(query="SELECT * FROM property_financials"):
    """
    Queries the database and returns a DataFrame.
    """
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
    return pd.read_sql(query, con=engine)
