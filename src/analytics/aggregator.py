import pandas as pd

def calculate_type_summary(df):
    """
    Calculates summary statistics by property type.
    """
    return df.groupby('type').agg({
        'price': 'mean',
        'area': 'mean'
    })

def calculate_yearly_trends(df):
    """
    Calculates yearly trends in property counts and total value.
    """
    return df.groupby('year').agg(
        property_count=('title', 'count'),
        total_value=('price', 'sum')
    )

def top_n_per_group(df, group_col, value_col, n=3):
    """
    Returns the top N properties per group by a specific value column.
    """
    return df.groupby(group_col).apply(
        lambda x: x.nlargest(n, value_col)
    ).reset_index(drop=True)
