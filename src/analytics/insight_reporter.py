def find_top_types_by_value(df):
    """
    Finds top property types by average price.
    """
    return df.groupby('type')['price'].mean().sort_values(ascending=False)

def calculate_price_per_sqft(df):
    """
    Calculates Price per Square Foot by property type.
    """
    # Avoid division by zero
    df['price_per_sqft'] = df['price'] / df['area'].replace(0, 1)
    return df.groupby('type')['price_per_sqft'].mean().sort_values(ascending=False)

def run_all_questions(df):
    """
    Prints a formatted summary of analytical findings.
    """
    print("\n--- Real Estate Analytical Insights ---")
    print("Top Property Types by Average Price:\n", find_top_types_by_value(df).head())
    print("\nTop Property Types by Price per Sqft:\n", calculate_price_per_sqft(df).head())
