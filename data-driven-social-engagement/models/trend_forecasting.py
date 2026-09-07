import pandas as pd
import numpy as np

def forecast_trends(df_trends, periods=7):
    """
    Forecasting using Simple Exponential Smoothing.
    Allows CSV data or generated demo data.
    """
    if df_trends is None or df_trends.empty:
        return None
        
    df = df_trends.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    forecasts = []
    
    for keyword in df['keyword'].unique():
        kw_data = df[df['keyword'] == keyword].sort_values(by='date')
        if len(kw_data) < 5:
            continue
            
        topic = kw_data['topic'].iloc[0]
        
        # Simple Exponential Smoothing (alpha=0.3)
        alpha = 0.3
        smoothed = [kw_data['search_volume'].iloc[0]]
        for val in kw_data['search_volume'].iloc[1:]:
            smoothed.append(alpha * val + (1 - alpha) * smoothed[-1])
            
        # Forecast is flat in simple ES, but we can project a slight trend
        recent_growth = (smoothed[-1] - smoothed[-5]) / max(smoothed[-5], 1)
        
        forecast_val = smoothed[-1] * (1 + recent_growth)
        
        if recent_growth > 0.05:
            status = "Rising"
        elif recent_growth < -0.05:
            status = "Declining"
        else:
            status = "Stable"
            
        forecasts.append({
            'keyword': keyword,
            'topic': topic,
            'current_volume': int(kw_data['search_volume'].iloc[-1]),
            'forecasted_volume': int(forecast_val),
            'recent_growth_rate': recent_growth,
            'trend_status': status
        })
        
    return pd.DataFrame(forecasts).sort_values(by='recent_growth_rate', ascending=False)
