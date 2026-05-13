import pandas as pd

def wide_to_long(df, id_vars, value_vars, var_name='metric', value_name='value'):
    """
    Converts data from wide to long format.
    """
    return df.melt(id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

def long_to_wide(df, index, columns, values):
    """
    Converts data from long to wide format.
    """
    return df.pivot(index=index, columns=columns, values=values)

def create_pivot_table(df, index, columns, values, aggfunc='mean', margins=True):
    """
    Builds an aggregated pivot table.
    """
    return df.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc, margins=margins)

def create_crosstab(df, index, columns):
    """
    Creates a cross-tabulation table.
    """
    return pd.crosstab(df[index], df[columns])
