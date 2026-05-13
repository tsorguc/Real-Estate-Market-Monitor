import matplotlib.pyplot as plt
import seaborn as sns
import os

def calculate_roi_by_genre(df):
    """
    Calculates ROI by primary genre: (Revenue - Budget) / Budget.
    """
    df['roi'] = (df['revenue_usd'] - df['budget_usd']) / df['budget_usd'].replace(0, 1)
    return df.groupby('primary_genre')['roi'].mean().sort_values(ascending=False)

def run_all_questions(df, output_dir="data/processed/analytics"):
    """
    Answers at least four quantified analytical questions and saves charts.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n--- Real Estate Analytical Insights (Lab 10) ---")
    
    # Question 1: Top genres by average revenue
    top_revenue = df.groupby('primary_genre')['revenue_usd'].mean().sort_values(ascending=False)
    print(f"1. Top Property Type by Revenue: {top_revenue.index[0]} (${top_revenue.iloc[0]:,.2f})")
    
    # Question 2: ROI by genre
    roi_stats = calculate_roi_by_genre(df)
    print(f"2. Most Profitable Type (ROI): {roi_stats.index[0]} ({roi_stats.iloc[0]:.2%})")
    
    # Question 3: Total listings per year
    yearly_volume = df.groupby('release_year')['listing_id'].count()
    print(f"3. Peak Year for Listings: {yearly_volume.idxmax()} ({yearly_volume.max()} properties)")
    
    # Question 4: Distribution of listings by genre
    genre_dist = df['primary_genre'].value_counts()
    print(f"4. Most Common Property Type: {genre_dist.idxmax()} ({genre_dist.max()} listings)")

    # Visualization: ROI by Genre
    plt.figure(figsize=(10, 6))
    roi_stats.plot(kind='bar', color='skyblue')
    plt.title('Average ROI by Property Type')
    plt.ylabel('ROI')
    plt.tight_layout()
    chart_path = os.path.join(output_dir, "genre_roi.png")
    plt.savefig(chart_path)
    print(f"\n✅ ROI Chart saved to {chart_path}")
