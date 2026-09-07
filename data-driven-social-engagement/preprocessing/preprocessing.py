import pandas as pd
import numpy as np

def clean_content_data(df):
    """
    Cleans and preprocesses the content performance dataset.
    """
    if df is None or df.empty:
        return df
        
    df = df.copy()
    
    # 1. Missing value handling
    df.fillna({
        'views': 0, 'likes': 0, 'comments': 0, 'shares': 0, 'saves': 0,
        'retention_rate': 0.0, 'hashtag_count': 0
    }, inplace=True)
    
    df.dropna(subset=['content_id', 'topic'], inplace=True)
    
    # 2. Duplicate removal
    df.drop_duplicates(subset=['content_id'], inplace=True)
    
    # 3. Invalid-value detection & datatype conversion
    numeric_cols = ['views', 'likes', 'comments', 'shares', 'saves', 'followers_before', 'followers_after']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        df[col] = df[col].apply(lambda x: max(0, x)) # No negative values
        
    # 4. Outlier detection (cap at 99th percentile for stable scaling)
    for col in ['views', 'likes', 'shares', 'saves']:
        q99 = df[col].quantile(0.99)
        if q99 > 0:
            df[f'{col}_capped'] = df[col].clip(upper=q99)
        else:
            df[f'{col}_capped'] = df[col]
            
    # Calculate Engagement Rate
    df['engagement_rate'] = np.where(df['views'] > 0, (df['likes'] + df['comments'] + df['shares'] + df['saves']) / df['views'], 0)
    
    return df

def clean_comments_data(df):
    if df is None or df.empty:
        return df
    
    df = df.copy()
    df.dropna(subset=['comment_id', 'text', 'content_id'], inplace=True)
    df.drop_duplicates(subset=['comment_id'], inplace=True)
    return df

def clean_trends_data(df):
    if df is None or df.empty:
        return df
        
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=['date', 'keyword'], inplace=True)
    df['search_volume'] = pd.to_numeric(df['search_volume'], errors='coerce').fillna(0).astype(int)
    return df
