import pandas as pd

def calculate_type_summary(df):
    """
    Calculates detailed summary statistics by primary genre (property type).
    Uses named aggregation with at least 4 different functions.
    """
    return df.groupby('primary_genre').agg(
        avg_revenue=('revenue_usd', 'mean'),
        total_revenue=('revenue_usd', 'sum'),
        property_count=('listing_id', 'count'),
        median_budget=('budget_usd', 'median')
    )

def calculate_yearly_trends(df):
    """
    Calculates yearly trends in property counts and total value.
    """
    return df.groupby('release_year').agg(
        property_count=('title', 'count'),
        total_revenue=('revenue_usd', 'sum')
    )

def top_n_per_group(df, group_col, value_col, n=3):
    """
    Returns the top N properties per group by a specific value column.
    """
    return df.groupby(group_col).apply(
        lambda x: x.nlargest(n, value_col)
    ).reset_index(drop=True)
