import pandas as pd

def demonstrate_melt(df):
    """
    Demonstrates melting wide data to long format using 3 numeric columns.
    As per Lab 10: budget_usd, revenue_usd, and we use area as a proxy for popularity.
    """
    # Ensure columns exist for demonstration
    if 'area' in df.columns:
        df = df.rename(columns={'area': 'popularity'})
    
    id_vars = ['listing_id', 'title', 'primary_genre']
    value_vars = ['budget_usd', 'revenue_usd', 'popularity']
    
    # Filter to only existing columns
    value_vars = [v for v in value_vars if v in df.columns]
    
    return df.melt(id_vars=id_vars, value_vars=value_vars, var_name='metric', value_name='value')

def create_genre_year_pivot(df):
    """
    Builds a pivot table showing revenue_usd broken down by release_year and primary_genre.
    Includes margins=True as per Lab 10.
    """
    return df.pivot_table(
        index='release_year', 
        columns='primary_genre', 
        values='revenue_usd', 
        aggfunc='mean', 
        margins=True
    )

def create_crosstab(df, index, columns):
    """
    Creates a cross-tabulation table.
    """
    return pd.crosstab(df[index], df[columns])
