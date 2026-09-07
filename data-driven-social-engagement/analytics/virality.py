import pandas as pd
import numpy as np

def calculate_viral_coefficient(df):
    """
    Calculates the custom Viral Coefficient based on engagement metrics.
    
    Formula:
    Viral Coefficient = (W_share * Shares + W_save * Saves + W_comment * Comments + W_retention * Retention_Contribution + W_growth * Follower_Contribution) / (Views + 1)
    
    Weights:
    - Shares: 5.0 (High value, direct virality)
    - Saves: 4.0 (High value, algorithmic signal)
    - Comments: 2.0 (Medium value, engagement)
    - Likes: 1.0 (Baseline, passive) -> not directly in numerator, but implicitly captured in views/baseline
    - Retention: scaled multiplier
    """
    if df is None or df.empty:
        return df
        
    df = df.copy()
    
    W_SHARE = 5.0
    W_SAVE = 4.0
    W_COMMENT = 2.0
    
    # Calculate base coefficient
    # Add smoothing to avoid division by zero
    views_smoothed = df['views'] + 1
    
    base_score = (
        (df['shares'] * W_SHARE) + 
        (df['saves'] * W_SAVE) + 
        (df['comments'] * W_COMMENT) + 
        (df['likes'] * 1.0)
    )
    
    # Retention Contribution (Retention rate acts as a multiplier: high retention boosts score)
    retention_multiplier = 1.0 + df['retention_rate']
    
    # Follower Growth Contribution (normalized growth relative to before)
    # Using np.where to handle 0 followers_before
    growth_rate = np.where(df['followers_before'] > 0, 
                           (df['followers_after'] - df['followers_before']) / df['followers_before'], 
                           0)
    
    # Cap growth multiplier to avoid explosion
    growth_multiplier = 1.0 + np.clip(growth_rate, 0, 1.0)
    
    # Final Formula
    df['viral_coefficient'] = (base_score / views_smoothed) * retention_multiplier * growth_multiplier
    
    # Normalize between 0 and a reasonable upper bound (e.g., 5.0)
    max_vc = df['viral_coefficient'].max()
    if max_vc > 0:
        # Scale to max ~ 5.0 for readability
        df['viral_coefficient'] = (df['viral_coefficient'] / max_vc) * 5.0
        
    return df

def calculate_rates(df):
    if df is None or df.empty:
        return df
    
    df = df.copy()
    views_smoothed = df['views'] + 1
    
    df['share_rate'] = df['shares'] / views_smoothed
    df['save_rate'] = df['saves'] / views_smoothed
    df['comment_rate'] = df['comments'] / views_smoothed
    df['like_rate'] = df['likes'] / views_smoothed
    df['save_to_share_ratio'] = np.where(df['shares'] > 0, df['saves'] / df['shares'], 0)
    
    return df
