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

def create_db_if_not_exists():
    """Creates the database if it doesn't already exist."""
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
    finally:
        connection.close()

def populate_financials(csv_path):
    """
    Reads the cleaned dataset and populates the 'property_financials' table.
    Includes budget and revenue for ROI calculations as per Lab 10 requirements.
    """
    # Ensure database exists
    create_db_if_not_exists()
    
    df = pd.read_csv(csv_path)
    
    # Map real estate columns to consistent names for analytics
    # Following Lab 10 requirement for financial columns (budget, revenue)
    # We use price to derive mock budget and revenue for the exercise
    df['budget_usd'] = df['price'] * 0.8
    df['revenue_usd'] = df['price']
    
    if 'collected_at' in df.columns:
        df['release_year'] = pd.to_datetime(df['collected_at']).dt.year
    else:
        df['release_year'] = datetime.now().year

    # Ensure we have the columns required by Lab 10 tasks
    mapping = {
        'listing_id': 'listing_id',
        'title': 'title',
        'budget_usd': 'budget_usd',
        'revenue_usd': 'revenue_usd',
        'release_year': 'release_year',
        'type': 'primary_genre' # Using 'type' as genre per Lab 10
    }
    
    # Rename for consistency with Lab 10 requirements
    df_to_save = df.rename(columns=mapping)
    
    # Keep only relevant columns
    required_columns = ['listing_id', 'title', 'budget_usd', 'revenue_usd', 'release_year', 'primary_genre']
    cols_to_use = [c for c in required_columns if c in df_to_save.columns]
    df_to_save = df_to_save[cols_to_use].dropna()
    
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
    df_to_save.to_sql('property_financials', con=engine, if_exists='replace', index=False)
    print(f"Successfully populated 'property_financials' table with {len(df_to_save)} records.")

def query_financials(query="SELECT * FROM property_financials"):
    """
    Queries the database and returns a DataFrame.
    """
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
    return pd.read_sql(query, con=engine)
