import pytest
import pandas as pd
from models.viral_prediction import ViralityPredictor

def test_virality_predictor_no_leakage():
    vp = ViralityPredictor()
    
    # Check that engagement metrics are NOT in the feature list
    leakage_features = ['views', 'likes', 'comments', 'shares', 'saves', 'retention_rate', 'viral_coefficient']
    for lf in leakage_features:
        assert lf not in vp.features
        
def test_virality_predictor_training():
    vp = ViralityPredictor()
    
    # Synthetic data
    df = pd.DataFrame({
        'platform': ['TikTok', 'Instagram', 'YouTube', 'TikTok'] * 25,
        'content_type': ['Video', 'Image', 'Video', 'Video'] * 25,
        'topic': ['Social Anxiety', 'Dating', 'Career', 'Social Anxiety'] * 25,
        'format': ['Short Video', 'Long Video'] * 50,
        'hook_type': ['Visual Hook'] * 100,
        'posting_time': ['Morning'] * 100,
        'cta_type': ['Share this'] * 100,
        'caption_style': ['Short'] * 100,
        'audience_segment': ['Gen Z'] * 100,
        'video_length': [30.0] * 100,
        'hashtag_count': [5] * 100,
        'viral_coefficient': [1.0, 2.0, 3.0, 4.0] * 25 # Outcome variable
    })
    
    metrics = vp.train_and_evaluate(df)
    
    assert metrics is not None
    assert 'accuracy' in metrics
    assert 'feature_importance' in metrics
