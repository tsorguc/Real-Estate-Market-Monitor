import os
import sys

# Detect interactive Jupyter/IPython environment safely
_in_notebook = False
try:
    from IPython import get_ipython
    if get_ipython() is not None:
        _in_notebook = True
except Exception:
    pass

if not _in_notebook and 'ipykernel' in sys.modules:
    _in_notebook = True

# Set Agg backend for non-interactive environments before importing pyplot
if not _in_notebook:
    import matplotlib
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def _save_fig(fig, output_dir, filename):
    """Internal helper to save figures in PNG and PDF formats."""
    os.makedirs(output_dir, exist_ok=True)
    png_path = os.path.join(output_dir, f"{filename}.png")
    pdf_path = os.path.join(output_dir, f"{filename}.pdf")
    
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    fig.savefig(pdf_path, bbox_inches='tight')
    if not _in_notebook:
        plt.close(fig)

def plot_top_properties_by_price(df, output_dir):
    """Horizontal bar chart for Top 10 properties by price."""
    # Ensure listing_id is string for labeling
    temp_df = df.nlargest(10, 'price').copy()
    temp_df['label'] = temp_df['title'].fillna('Property ' + temp_df['listing_id'].astype(str))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=temp_df, 
        y='label', 
        x='price', 
        hue='label',
        palette='viridis', 
        ax=ax,
        legend=False
    )
    
    # Add annotations in USD Millions
    for i, p in enumerate(ax.patches):
        width = p.get_width()
        ax.text(width, p.get_y() + p.get_height()/2, 
                f' ${width/1e6:.1f}M', 
                va='center')
    
    ax.set_title("Top 10 Most Expensive Properties", fontsize=14, pad=20)
    ax.set_xlabel("Price (USD)")
    ax.set_ylabel("")
    
    _save_fig(fig, output_dir, "top_10_properties_price")

def plot_avg_price_over_time(df, output_dir):
    """Dual-axis chart: Avg Price (Line) and Listing Count (Bar) over time."""
    # Prepare data
    df['collected_at'] = pd.to_datetime(df['collected_at'])
    ts_data = df.resample('D', on='collected_at').agg({
        'price': 'mean',
        'listing_id': 'count'
    }).rename(columns={'listing_id': 'count'}).dropna()
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Primary axis: Count
    ax1.bar(ts_data.index, ts_data['count'], color='lightgrey', alpha=0.5, label='Listing Count')
    ax1.set_ylabel("Number of Listings")
    ax1.set_xlabel("Collection Date")
    
    # Secondary axis: Price
    ax2 = ax1.twinx()
    ax2.plot(ts_data.index, ts_data['price'], color='tab:red', marker='o', label='Avg Price')
    ax2.set_ylabel("Average Price (USD)")
    
    fig.suptitle("Market Trends: Volume vs. Average Price", fontsize=14)
    fig.legend(loc="upper left", bbox_to_anchor=(0.15, 0.85))
    
    _save_fig(fig, output_dir, "market_trends_dual_axis")

def plot_price_distribution(df, output_dir):
    """Histogram of property prices."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['price'], bins=30, kde=True, color='skyblue', ax=ax)
    ax.set_title("Distribution of Property Prices", fontsize=14)
    ax.set_xlabel("Price (USD)")
    _save_fig(fig, output_dir, "price_distribution")

def plot_area_vs_price(df, output_dir):
    """Scatter plot of Area vs. Price."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='area', y='price', hue='type', alpha=0.6, ax=ax)
    ax.set_title("Property Area vs. Price", fontsize=14)
    ax.set_xlabel("Area (sqft)")
    ax.set_ylabel("Price (USD)")
    _save_fig(fig, output_dir, "area_vs_price")

def plot_property_type_counts(df, output_dir):
    """Bar chart of listing counts by property type."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x='type', hue='type', palette='Set2', ax=ax, legend=False)
    ax.set_title("Listing Counts by Property Type", fontsize=14)
    ax.set_xlabel("Property Type")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    _save_fig(fig, output_dir, "property_type_counts")

def plot_price_by_type_boxplot(df, output_dir):
    """Boxplot of prices by property type."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x='type', y='price', hue='type', palette='Pastel1', ax=ax, legend=False)
    ax.set_title("Price Distribution by Property Type", fontsize=14)
    ax.set_xlabel("Property Type")
    ax.set_ylabel("Price (USD)")
    plt.xticks(rotation=45)
    _save_fig(fig, output_dir, "price_by_type_boxplot")

def plot_correlation_heatmap(df, output_dir):
    """Heatmap of numerical feature correlations."""
    numeric_df = df.select_dtypes(include=[np.number])
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Feature Correlation Heatmap", fontsize=14)
    _save_fig(fig, output_dir, "correlation_heatmap")

def plot_dashboard_subplots(df, output_dir):
    """2x2 Dashboard combining key metrics."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 0,0: Type Counts
    sns.countplot(data=df, x='type', hue='type', palette='Set2', ax=axes[0, 0], legend=False)
    axes[0, 0].set_title("Market Composition")
    axes[0, 0].tick_params(axis='x', rotation=30)
    
    # 0,1: Area vs Price
    sns.scatterplot(data=df, x='area', y='price', hue='type', alpha=0.6, ax=axes[0, 1])
    axes[0, 1].set_title("Area vs. Price")
    
    # 1,0: Price Dist
    sns.histplot(df['price'], bins=20, kde=True, color='green', ax=axes[1, 0])
    axes[1, 0].set_title("Price Distribution")
    
    # 1,1: Avg Price by Type
    avg_price = df.groupby('type')['price'].mean().sort_values()
    avg_price.plot(kind='barh', ax=axes[1, 1], color='orange')
    axes[1, 1].set_title("Average Price by Type")
    
    fig.suptitle("Real Estate Market Executive Dashboard", fontsize=20, y=0.95)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    _save_fig(fig, output_dir, "executive_dashboard_static")
