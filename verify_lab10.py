import os
import sys
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

try:
    from src.analytics import db_connector, aggregator, pivot_builder, time_series, insight_reporter
    print("✅ Module Imports: SUCCESS")
except ImportError as e:
    print(f"❌ Module Imports: FAILED ({e})")
    sys.exit(1)

def verify():
    print("\n--- Lab 10 Final Verification ---")

    # 1. MySQL Connectivity
    try:
        df_fin = db_connector.query_financials()
        if not df_fin.empty and 'budget_usd' in df_fin.columns:
            print(f"✅ Requirement 1 (MySQL): SUCCESS ({len(df_fin)} records found)")
        else:
            print("❌ Requirement 1 (MySQL): FAILED (Table empty or missing columns)")
    except Exception as e:
        print(f"❌ Requirement 1 (MySQL): FAILED ({e})")

    # 2. CSV Reports
    reports = [
        'data/processed/analytics/genre_analysis.csv',
        'data/processed/analytics/pivot_genre_year.csv',
        'data/processed/analytics/time_series_rolling.csv',
        'data/processed/analytics/yearly_trends.csv'
    ]
    all_reports = True
    for r in reports:
        if os.path.exists(r):
            print(f"✅ Report Found: {r}")
        else:
            print(f"❌ Report Missing: {r}")
            all_reports = False
    
    if all_reports:
        print("✅ Requirement 2 (CSV Reports): SUCCESS")

    # 3. Aggregation Check
    try:
        df_agg = pd.read_csv('data/processed/analytics/genre_analysis.csv')
        expected_cols = ['avg_revenue', 'total_revenue', 'property_count', 'median_budget']
        if all(c in df_agg.columns for c in expected_cols):
            print("✅ Requirement 4 (GroupBy Aggregations): SUCCESS")
        else:
            print("❌ Requirement 4 (GroupBy Aggregations): FAILED (Missing named aggregations)")
    except Exception:
        print("❌ Requirement 4: FAILED (Could not read analysis file)")

    # 4. Chart Check
    if os.path.exists('data/processed/analytics/genre_roi.png'):
        print("✅ Requirement 8 (ROI Chart): SUCCESS")
    else:
        print("❌ Requirement 8 (ROI Chart): FAILED")

    print("\n🏁 Verification Complete. If all checks passed, your Lab 10 is ready!")

if __name__ == "__main__":
    verify()
