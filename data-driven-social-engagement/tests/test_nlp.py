import pytest
from models.sentiment_model import get_sentiment
from models.relatability import detect_relatability

def test_sentiment_positive():
    label, score = get_sentiment("I love this so much, it is amazing!")
    assert label == "Positive"
    assert score > 0

def test_sentiment_negative():
    label, score = get_sentiment("This is terrible and I hate it.")
    assert label == "Negative"
    assert score < 0
    
def test_relatability_detection():
    # Test strong trigger
    label, score, p_score, exp = detect_relatability("This is exactly me, I struggle with this daily.")
    assert label == "Relatable"
    assert score >= 0.5
    
    # Test neutral
    label, score, p_score, exp = detect_relatability("Cool video man.")
    assert label == "Neutral"
    assert score < 0.5
