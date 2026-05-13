import pandas as pd

def parse_release_dates(df, date_col='collected_at'):
    """
    Parses date column and extracts components (year, month, weekday) as per Lab 10.
    """
    df[date_col] = pd.to_datetime(df[date_col])
    df['release_year'] = df[date_col].dt.year
    df['release_month'] = df[date_col].dt.month
    df['release_weekday'] = df[date_col].dt.weekday
    return df

def build_time_series_analysis(df, date_col='collected_at', value_col='revenue_usd'):
    """
    Builds monthly series, resamples to yearly, and computes rolling averages.
    """
    df_ts = df.copy()
    df_ts[date_col] = pd.to_datetime(df_ts[date_col])
    df_ts = df_ts.set_index(date_col).sort_index()
    
    # Monthly resample
    monthly_series = df_ts[value_col].resample('ME').sum()
    
    # Yearly resample
    yearly_series = df_ts[value_col].resample('YE').sum()
    
    # Rolling averages (3, 6, 12)
    rolling_results = pd.DataFrame(monthly_series)
    for window in [3, 6, 12]:
        rolling_results[f'rolling_{window}_mo'] = monthly_series.rolling(window=window).mean()
        
    return monthly_series, yearly_series, rolling_results
