import pytest
import pandas as pd
import numpy as np
from experiments.ab_testing import run_ab_test
from recommender.strategy_recommender import generate_recommendations
from models.trend_forecasting import forecast_trends

def test_recommender():
    df = pd.DataFrame({
        'topic': ['A', 'A', 'B', 'B'],
        'format': ['Short', 'Long', 'Short', 'Long'],
        'hook_type': ['Visual', 'Visual', 'Text', 'Text'],
        'posting_time': ['Morning', 'Evening', 'Morning', 'Evening'],
        'cta_type': ['Share', 'Save', 'Share', 'Save'],
        'viral_coefficient': [1.5, 1.2, 0.8, 0.9],
        'platform': ['TikTok'] * 4,
        'content_type': ['Video'] * 4,
        'video_length': [15.0] * 4,
        'caption_style': ['Short'] * 4,
        'hashtag_count': [3, 4, 3, 5],
        'audience_segment': ['Gen Z'] * 4
    })
    
    recs = generate_recommendations(df)
    
    assert recs is not None
    assert 'top_strategies' in recs
    assert len(recs['top_strategies']) > 0
    
    top_strat = recs['top_strategies'][0]
    assert top_strat['best_topic']['value'] == 'A'
    assert 'expected_metric' in top_strat
