import pandas as pd
import numpy as np
from scipy import stats

def run_ab_test(df, variable_col, control_val, treatment_val, metric_col):
    """
    Runs a statistical A/B test.
    Handles continuous metrics (t-test or Mann-Whitney U depending on normality assumption).
    For simplicity and reliable handling of skewed social media data, we use Mann-Whitney U for engagement metrics,
    and t-test for well-behaved continuous data like retention rate if normally distributed.
    Here we default to Mann-Whitney U for engagement metrics (likes, shares, views) due to right-skewness,
    and Welch's t-test for bounded metrics like retention.
    """
    if df is None or df.empty:
        return None
        
    df = df.dropna(subset=[variable_col, metric_col])
    
    control_data = df[df[variable_col] == control_val][metric_col]
    treatment_data = df[df[variable_col] == treatment_val][metric_col]
    
    n_control = len(control_data)
    n_treatment = len(treatment_data)
    
    if n_control < 5 or n_treatment < 5:
        return {
            "error": "Insufficient sample size (minimum 5 per group required)."
        }
        
    if df[metric_col].dtype == 'object' or df[metric_col].dtype.name == 'category':
        # Chi-square test for categorical metrics
        df_filtered = df[df[variable_col].isin([control_val, treatment_val])]
        contingency_table = pd.crosstab(df_filtered[variable_col], df_filtered[metric_col])
        
        # We need at least 2 categories and valid contingency table
        if contingency_table.shape[0] < 2 or contingency_table.shape[1] < 2:
            return {"error": "Insufficient category variations for Chi-square test."}
            
        stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        significant = p_value < 0.05
        
        return {
            "variable": variable_col,
            "control": control_val,
            "treatment": treatment_val,
            "metric": metric_col,
            "n_control": n_control,
            "n_treatment": n_treatment,
            "chi_square_statistic": stat,
            "p_value": p_value,
            "test_used": "Chi-square test",
            "statistically_significant": significant,
            "winner": "Difference detected (Categorical)" if significant else "No Clear Winner"
        }
        
    mean_control = control_data.mean()
    mean_treatment = treatment_data.mean()
    
    diff = mean_treatment - mean_control
    pct_improvement = (diff / mean_control * 100) if mean_control > 0 else 0
    
    # Choose test based on metric type
    if metric_col in ['retention_rate', 'engagement_rate', 'viral_coefficient']:
        # Welch's t-test (doesn't assume equal variance)
        stat, p_value = stats.ttest_ind(treatment_data, control_data, equal_var=False)
        test_used = "Welch's t-test"
    else:
        # Mann-Whitney U for highly skewed count data
        stat, p_value = stats.mannwhitneyu(treatment_data, control_data, alternative='two-sided')
        test_used = "Mann-Whitney U test"
        
    # Calculate confidence interval for the difference in means (approximate using t-distribution)
    se = np.sqrt(control_data.var(ddof=1)/n_control + treatment_data.var(ddof=1)/n_treatment)
    t_crit = stats.t.ppf(0.975, df=min(n_control, n_treatment)-1)
    ci_lower = diff - t_crit * se
    ci_upper = diff + t_crit * se
    
    # Calculate confidence interval for the individual means
    se_control = np.sqrt(control_data.var(ddof=1)/n_control) if n_control > 1 else 0
    t_crit_control = stats.t.ppf(0.975, df=n_control-1) if n_control > 1 else 0
    ci_control_margin = t_crit_control * se_control
    
    se_treatment = np.sqrt(treatment_data.var(ddof=1)/n_treatment) if n_treatment > 1 else 0
    t_crit_treatment = stats.t.ppf(0.975, df=n_treatment-1) if n_treatment > 1 else 0
    ci_treatment_margin = t_crit_treatment * se_treatment
    
    significant = p_value < 0.05
    
    if significant:
        winner = treatment_val if diff > 0 else control_val
    else:
        winner = "No Clear Winner"
        
    return {
        "variable": variable_col,
        "control": control_val,
        "treatment": treatment_val,
        "metric": metric_col,
        "n_control": n_control,
        "n_treatment": n_treatment,
        "mean_control": mean_control,
        "mean_treatment": mean_treatment,
        "ci_control_margin": ci_control_margin,
        "ci_treatment_margin": ci_treatment_margin,
        "absolute_difference": diff,
        "percentage_improvement": pct_improvement,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "test_used": test_used,
        "statistically_significant": significant,
        "winner": winner
    }
