import pytest
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def test_datasets_exist_and_sufficient():
    # 7. DATASET VALIDATION
    content_file = os.path.join(DATA_DIR, 'content_performance.csv')
    comments_file = os.path.join(DATA_DIR, 'comments.csv')
    trends_file = os.path.join(DATA_DIR, 'trends.csv')
    
    assert os.path.exists(content_file), "content_performance.csv is missing"
    assert os.path.exists(comments_file), "comments.csv is missing"
    assert os.path.exists(trends_file), "trends.csv is missing"
    
    df_content = pd.read_csv(content_file)
    df_comments = pd.read_csv(comments_file)
    df_trends = pd.read_csv(trends_file)
    
    # >= 500 records for content
    assert len(df_content) >= 500, f"content_performance.csv has {len(df_content)} records, expected >= 500"
    
    # Substantial comments dataset (typically ~3x content)
    assert len(df_comments) >= len(df_content), "comments.csv should have substantial data"
    
    # Trends should have history
    assert len(df_trends) >= 30, "trends.csv lacks sufficient historical observations"
