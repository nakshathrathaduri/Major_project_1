import pytest
import pandas as pd
from experiments.ab_testing import run_ab_test

def test_run_ab_test_welchs():
    # Create synthetic continuous data for Welch's t-test
    df = pd.DataFrame({
        'format': ['Short'] * 50 + ['Long'] * 50,
        'retention_rate': [0.5] * 50 + [0.8] * 50  # Long format has significantly higher retention
    })
    
    result = run_ab_test(df, 'format', 'Short', 'Long', 'retention_rate')
    
    assert 'error' not in result
    assert result['test_used'] == "Welch's t-test"
    assert result['mean_control'] == pytest.approx(0.5)
    assert result['mean_treatment'] == pytest.approx(0.8)
    assert result['statistically_significant'] == True
    assert result['winner'] == 'Long'
    
    # 2. Chi-square test
    df_cat = pd.DataFrame({
        'format': ['Short'] * 50 + ['Long'] * 50,
        'virality_tier': ['HIGH'] * 40 + ['LOW'] * 10 + ['HIGH'] * 10 + ['LOW'] * 40
    })
    df_cat['virality_tier'] = df_cat['virality_tier'].astype('category')
    
    result_cat = run_ab_test(df_cat, 'format', 'Short', 'Long', 'virality_tier')
    
    assert 'error' not in result_cat
    assert result_cat['test_used'] == "Chi-square test"
    assert 'chi_square_statistic' in result_cat
    assert bool(result_cat['statistically_significant']) is True
    assert result_cat['winner'] == 'Difference detected (Categorical)'

def test_run_ab_test_mann_whitney():
    # Create synthetic count data for Mann-Whitney U test
    df = pd.DataFrame({
        'hook_type': ['Visual'] * 50 + ['Text'] * 50,
        'shares': [10] * 50 + [100] * 50  # Text hook has significantly higher shares
    })
    
    result = run_ab_test(df, 'hook_type', 'Visual', 'Text', 'shares')
    
    assert 'error' not in result
    assert result['test_used'] == "Mann-Whitney U test"
    assert bool(result['statistically_significant']) is True
    assert result['winner'] == 'Text'

