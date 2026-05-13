import pandas as pd

def parse_dates(df, date_col):
    """
    Parses a date column to datetime format and extracts components.
    """
    df[date_col] = pd.to_datetime(df[date_col])
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['weekday'] = df[date_col].dt.weekday
    return df

def resample_data(df, date_col, freq='Y'):
    """
    Resamples time series data to a specified frequency.
    """
    return df.set_index(date_col).resample(freq).sum()

def calculate_rolling_averages(df, col, windows=[3, 6, 12]):
    """
    Computes rolling averages for specified window sizes.
    """
    for window in windows:
        df[f'rolling_{window}_mo'] = df[col].rolling(window=window).mean()
    return df
