import pytest
import pandas as pd
import numpy as np
from models.trend_forecasting import forecast_trends

def test_forecasting():
    # Need at least 5 points for a keyword
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'keyword': ['anxiety'] * 10,
        'topic': ['Mental Health'] * 10,
        'search_volume': [100, 110, 120, 130, 150, 180, 200, 250, 300, 350]
    })
    
    forecasts = forecast_trends(df)
    
    assert forecasts is not None
    assert not forecasts.empty
    assert forecasts['trend_status'].iloc[0] == 'Rising'
