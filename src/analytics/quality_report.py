import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.utils.logger import logging

def generate_quality_report(df):
    """
    Generates a data quality report.
    As per Lab 8 Requirements.
    """
    logging.info("--- Data Quality Assessment ---")
    
    # 1. Missing Value Analysis
    missing_counts = df.isnull().sum()
    missing_percentages = (df.isnull().sum() / len(df)) * 100
    
    quality_df = pd.DataFrame({
        'missing_count': missing_counts,
        'missing_percentage': missing_percentages
    })
    
    # 2. Severity Scoring (Simplified: high if > 20% missing)
    quality_df['severity'] = np.where(quality_df['missing_percentage'] > 20, 'High', 
                                    np.where(quality_df['missing_percentage'] > 5, 'Medium', 'Low'))
    
    # 3. Detect zero-as-missing patterns
    # For numeric columns, count zeros
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    quality_df['zero_counts'] = 0
    for col in numeric_cols:
        quality_df.loc[col, 'zero_counts'] = (df[col] == 0).sum()

    # 4. IQR-based outlier detection for numeric columns
    quality_df['outlier_count'] = 0
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        quality_df.loc[col, 'outlier_count'] = len(outliers)
        
    # 5. Visualizing missing data pattern (Heatmap)
    os.makedirs("data/processed/analytics/charts", exist_ok=True)
    heatmap_path = "data/processed/analytics/charts/missing_data_heatmap.png"
    
    if not df.empty:
        plt.figure(figsize=(12, 8))
        # Simple heatmap representation using matplotlib, explicitly casting to int
        plt.imshow(df.isnull().astype(int), aspect='auto', cmap='viridis', interpolation='nearest')
        plt.title('Missing Data Heatmap')
        plt.xlabel('Columns')
        plt.ylabel('Rows')
        plt.colorbar(label='Missing (1/Yellow) vs Present (0/Purple)')
        plt.tight_layout()
        plt.savefig(heatmap_path)
        plt.close()
        logging.info(f"Saved heatmap: {heatmap_path}")
    else:
        logging.warning("DataFrame is empty, skipping heatmap generation.")
    
    # 6. Save full quality report as CSV
    os.makedirs("data/processed/analytics", exist_ok=True)
    report_path = "data/processed/analytics/data_quality_report.csv"
    quality_df.to_csv(report_path)
    logging.info(f"Saved quality report: {report_path}")
    
    print(f"✅ Data Quality Report saved to {report_path}")
    return quality_df
