import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

try:
    from src.visualization.static_charts import (
        plot_top_properties_by_price,
        plot_avg_price_over_time,
        plot_price_distribution,
        plot_area_vs_price,
        plot_property_type_counts,
        plot_price_by_type_boxplot,
        plot_correlation_heatmap,
        plot_dashboard_subplots
    )
    from src.visualization.interactive_charts import (
        plot_interactive_price_scatter,
        plot_interactive_type_distribution,
        plot_interactive_price_by_type,
        plot_interactive_area_hist,
        plot_interactive_multi_layout
    )
    from src.visualization.chart_generator import run_visualization_pipeline
    print("[OK] Module Imports: SUCCESS")
except ImportError as e:
    print(f"[ERROR] Module Imports: FAILED ({e})")
    sys.exit(1)

def verify():
    print("\n--- Lab 12 Final Verification ---")

    # 1. Check Static Charts Outputs
    print("\nChecking Static Charts (Matplotlib/Seaborn)...")
    static_dir = "outputs/visualizations/static"
    static_charts = [
        "top_10_properties_price",
        "market_trends_dual_axis",
        "price_distribution",
        "area_vs_price",
        "property_type_counts",
        "price_by_type_boxplot",
        "correlation_heatmap",
        "executive_dashboard_static"
    ]
    
    missing_static = []
    for chart in static_charts:
        png_path = os.path.join(static_dir, f"{chart}.png")
        pdf_path = os.path.join(static_dir, f"{chart}.pdf")
        
        png_ok = os.path.exists(png_path)
        pdf_ok = os.path.exists(pdf_path)
        
        if png_ok and pdf_ok:
            print(f"  [OK] {chart} (PNG & PDF): FOUND")
        else:
            print(f"  [ERROR] {chart}: MISSING (PNG: {'OK' if png_ok else 'MISSING'}, PDF: {'OK' if pdf_ok else 'MISSING'})")
            missing_static.append(chart)
            
    if not missing_static:
        print("[OK] Requirement 1 (8 Static Charts - PNG & PDF): SUCCESS")
    else:
        print("[ERROR] Requirement 1 (8 Static Charts - PNG & PDF): FAILED")

    # 2. Check Interactive Charts Outputs
    print("\nChecking Interactive Charts (Plotly)...")
    interactive_dir = "outputs/visualizations/interactive"
    interactive_charts = [
        "interactive_price_scatter",
        "interactive_type_pie",
        "interactive_price_violin",
        "interactive_area_histogram",
        "interactive_multi_layout"
    ]
    
    missing_interactive = []
    for chart in interactive_charts:
        html_path = os.path.join(interactive_dir, f"{chart}.html")
        html_ok = os.path.exists(html_path)
        
        if html_ok:
            print(f"  [OK] {chart} (HTML): FOUND")
        else:
            print(f"  [ERROR] {chart}: MISSING")
            missing_interactive.append(chart)
            
    if not missing_interactive:
        print("[OK] Requirement 2 (5 Interactive HTML Charts): SUCCESS")
    else:
        print("[ERROR] Requirement 2 (5 Interactive HTML Charts): FAILED")

    # 3. Check CLI Script
    print("\nChecking CLI Entry Point...")
    cli_path = "scripts/generate_visualizations.py"
    if os.path.exists(cli_path):
        print(f"  [OK] {cli_path}: FOUND")
        print("[OK] Requirement 3 (CLI Script): SUCCESS")
    else:
        print(f"  [ERROR] {cli_path}: MISSING")
        print("[ERROR] Requirement 3 (CLI Script): FAILED")

    # 4. Check Submission Notebook
    print("\nChecking Submission Notebook...")
    notebook_path = "notebooks/lab12_visualization.ipynb"
    if os.path.exists(notebook_path):
        print(f"  [OK] {notebook_path}: FOUND")
        print("[OK] Requirement 4 (Jupyter Notebook): SUCCESS")
    else:
        print(f"  [ERROR] {notebook_path}: MISSING")
        print("[ERROR] Requirement 4 (Jupyter Notebook): FAILED")

    print("\n*** Lab 12 Verification Complete! ***")

if __name__ == "__main__":
    verify()
