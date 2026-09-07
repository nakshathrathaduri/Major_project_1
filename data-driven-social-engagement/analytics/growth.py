import pandas as pd

def calculate_growth_metrics(df):
    """
    Calculates follower growth metrics for each piece of content.
    """
    df_calc = df.copy()
    
    if 'followers_before' in df_calc.columns and 'followers_after' in df_calc.columns:
        df_calc['growth_absolute'] = df_calc['followers_after'] - df_calc['followers_before']
        
        # Avoid division by zero
        before = df_calc['followers_before'].replace(0, 1)
        df_calc['growth_rate'] = (df_calc['growth_absolute'] / before).fillna(0)
    
    return df_calc

def aggregate_growth_by_topic(df):
    """
    Aggregates growth metrics by content topic.
    """
    if 'growth_absolute' not in df.columns:
        df = calculate_growth_metrics(df)
        
    if 'topic' not in df.columns:
        return pd.DataFrame()
        
    return df.groupby('topic')[['growth_absolute', 'growth_rate']].mean().reset_index()

def aggregate_growth_over_time(df, time_col='content_date'):
    """
    Aggregates growth metrics over time.
    """
    if 'growth_absolute' not in df.columns:
        df = calculate_growth_metrics(df)
        
    if time_col not in df.columns:
        return pd.DataFrame()
        
    df_time = df.copy()
    df_time[time_col] = pd.to_datetime(df_time[time_col])
    
    # Sort and calculate cumulative growth
    df_time = df_time.sort_values(time_col)
    df_time['cumulative_growth'] = df_time['growth_absolute'].cumsum()
    
    return df_time[[time_col, 'growth_absolute', 'cumulative_growth', 'topic']]
