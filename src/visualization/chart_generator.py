import os
import pandas as pd
from .static_charts import (
    plot_top_properties_by_price,
    plot_avg_price_over_time,
    plot_price_distribution,
    plot_area_vs_price,
    plot_property_type_counts,
    plot_price_by_type_boxplot,
    plot_correlation_heatmap,
    plot_dashboard_subplots
)
from .interactive_charts import (
    plot_interactive_price_scatter,
    plot_interactive_type_distribution,
    plot_interactive_price_by_type,
    plot_interactive_area_hist,
    plot_interactive_multi_layout
)

def run_visualization_pipeline(data_path, static_dir, interactive_dir):
    """
    Loads data and runs all visualization functions.
    """
    print(f"Loading data from {data_path}...")
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    
    # Static Charts
    print("Generating static charts...")
    static_functions = [
        plot_top_properties_by_price,
        plot_avg_price_over_time,
        plot_price_distribution,
        plot_area_vs_price,
        plot_property_type_counts,
        plot_price_by_type_boxplot,
        plot_correlation_heatmap,
        plot_dashboard_subplots
    ]
    
    for i, func in enumerate(static_functions, 1):
        print(f"  [{i}/{len(static_functions)}] Running {func.__name__}...")
        func(df, static_dir)
        
    # Interactive Charts
    print("Generating interactive charts...")
    interactive_functions = [
        plot_interactive_price_scatter,
        plot_interactive_type_distribution,
        plot_interactive_price_by_type,
        plot_interactive_area_hist,
        plot_interactive_multi_layout
    ]
    
    for i, func in enumerate(interactive_functions, 1):
        print(f"  [{i}/{len(interactive_functions)}] Running {func.__name__}...")
        func(df, interactive_dir)
        
    print("Visualization pipeline completed successfully.")

if __name__ == "__main__":
    # Example usage for testing
    DATA_PATH = "data/processed/cleaned/cleaned_data.csv"
    STATIC_DIR = "outputs/visualizations/static"
    INTERACTIVE_DIR = "outputs/visualizations/interactive"
    run_visualization_pipeline(DATA_PATH, STATIC_DIR, INTERACTIVE_DIR)
