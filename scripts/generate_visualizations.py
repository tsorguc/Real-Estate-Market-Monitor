import os
import sys
import argparse

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.visualization.chart_generator import run_visualization_pipeline

def main():
    parser = argparse.ArgumentParser(description="Generate static and interactive visualizations for Real Estate Market Monitor.")
    parser.add_argument(
        "--data", 
        type=str, 
        default="data/processed/cleaned/cleaned_data.csv",
        help="Path to the cleaned CSV data file."
    )
    parser.add_argument(
        "--static-out", 
        type=str, 
        default="outputs/visualizations/static",
        help="Directory to save static charts (PNG/PDF)."
    )
    parser.add_argument(
        "--interactive-out", 
        type=str, 
        default="outputs/visualizations/interactive",
        help="Directory to save interactive charts (HTML)."
    )
    
    args = parser.parse_args()
    
    # Ensure directories exist
    os.makedirs(args.static_out, exist_ok=True)
    os.makedirs(args.interactive_out, exist_ok=True)
    
    try:
        run_visualization_pipeline(
            data_path=args.data,
            static_dir=args.static_out,
            interactive_dir=args.interactive_out
        )
    except Exception as e:
        print(f"Failed to generate visualizations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
