import pandas as pd

def merge_datasets(df1, df2, on_key, how='inner'):
    """
    Merges two DataFrames on a specified key.
    """
    return pd.merge(df1, df2, on=on_key, how=how)

def concat_datasets(df_list, axis=0):
    """
    Concatenates a list of DataFrames.
    """
    return pd.concat(df_list, axis=axis)

def compare_joins(df1, df2, on_key):
    """
    Demonstrates inner, left, right, and outer joins and returns their row counts.
    """
    join_types = ['inner', 'left', 'right', 'outer']
    results = {}
    for join_type in join_types:
        merged = pd.merge(df1, df2, on=on_key, how=join_type)
        results[join_type] = len(merged)
        print(f"{join_type.capitalize()} join row count: {len(merged)}")
    return results
