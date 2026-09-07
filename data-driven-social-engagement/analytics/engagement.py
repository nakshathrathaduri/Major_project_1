import pandas as pd

def calculate_engagement_metrics(df):
    """
    Calculates foundational engagement metrics.
    """
    df_calc = df.copy()
    
    # Avoid division by zero
    views = df_calc['views'].replace(0, 1)
    
    df_calc['engagement_rate'] = ((df_calc['likes'] + df_calc['comments'] + df_calc['shares'] + df_calc['saves']) / views).fillna(0)
    df_calc['share_rate'] = (df_calc['shares'] / views).fillna(0)
    df_calc['save_rate'] = (df_calc['saves'] / views).fillna(0)
    df_calc['comment_rate'] = (df_calc['comments'] / views).fillna(0)
    
    # Save to share ratio indicates whether content is informational (saves) vs relatable/social (shares)
    shares = df_calc['shares'].replace(0, 1)
    df_calc['save_to_share_ratio'] = (df_calc['saves'] / shares).fillna(0)
    
    return df_calc
