import pytest
import pandas as pd
import numpy as np
from analytics.virality import calculate_viral_coefficient
from experiments.ab_testing import run_ab_test

def test_calculate_viral_coefficient():
    # Setup simple dataframe
    data = {
        'views': [1000],
        'likes': [100],
        'comments': [10],
        'shares': [50],
        'saves': [20],
        'retention_rate': [0.5],
        'followers_before': [1000],
        'followers_after': [1050]
    }
    df = pd.DataFrame(data)
    
    result = calculate_viral_coefficient(df)
    
    assert 'viral_coefficient' in result.columns
    # Check that score is > 0
    assert result['viral_coefficient'].iloc[0] > 0

def test_ab_testing_significance():
    # Create synthetic data where treatment is obviously better
    np.random.seed(42)
    control = np.random.normal(10, 2, 50)
    treatment = np.random.normal(20, 2, 50)
    
    df = pd.DataFrame({
        'group': ['control']*50 + ['treatment']*50,
        'metric': np.concatenate([control, treatment])
    })
    
    # Run test
    # Welch's t-test path is triggered by using 'retention_rate' as col name
    result = run_ab_test(df, 'group', 'control', 'treatment', 'metric')
    
    assert result is not None
    assert 'p_value' in result
    assert bool(result['statistically_significant']) is True
    assert result['winner'] == 'treatment'
    
def test_ab_testing_insufficient_sample():
    df = pd.DataFrame({
        'group': ['control', 'treatment'],
        'metric': [10, 20]
    })
    result = run_ab_test(df, 'group', 'control', 'treatment', 'metric')
    assert "error" in result
