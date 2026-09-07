import pandas as pd

def calculate_correlations(df, columns):
    """
    Calculates Pearson correlation matrix for specified numerical columns.
    """
    existing_cols = [col for col in columns if col in df.columns]
    if not existing_cols:
        return pd.DataFrame()
        
    return df[existing_cols].corr()

def get_top_correlations(df, target_metric, columns=None, n=5):
    """
    Returns the top features correlated with a target metric.
    """
    if columns:
        corr_matrix = calculate_correlations(df, columns + [target_metric])
    else:
        # Use all numerical columns
        num_df = df.select_dtypes(include=['number'])
        corr_matrix = num_df.corr()
        
    if target_metric not in corr_matrix.columns:
        return pd.Series()
        
    # Get correlations with target, drop the target itself, take absolute values, sort
    corrs = corr_matrix[target_metric].drop(target_metric)
    # Return original signs but sorted by absolute magnitude
    return corrs.reindex(corrs.abs().sort_values(ascending=False).index).head(n)
