import streamlit as st
import plotly.express as px
from models.trend_forecasting import forecast_trends

def render_trends(df_trends):
    st.title("Trend Forecasting")
    st.markdown("The forecast estimates the recent direction of a trend and classifies it as Rising, Stable, or Declining.")
    
    st.info("💡 **Mode**: Currently using Demo/Synthetic Trend Mode. You can upload external API CSVs to use real data. The forecasting logic remains the same.")
    
    uploaded_file = st.file_uploader("Upload External Trend CSV (Columns: date, keyword, topic, search_volume)", type="csv")
    
    if uploaded_file is not None:
        import pandas as pd
        try:
            df_trends = pd.read_csv(uploaded_file)
            st.success("✅ External Data Loaded Successfully")
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
            return
    else:
        st.caption("Using Default Demo/Synthetic Data")
    
    if df_trends is None or df_trends.empty:
        st.warning("No trend data available.")
        return
        
    forecasts = forecast_trends(df_trends)
    
    if forecasts is None or forecasts.empty:
        st.warning("Not enough data to run forecasts.")
        return
        
    st.markdown("---")
    st.subheader("Emerging Relatable Struggles")
    
    # Display cards for top 3 rising
    rising = forecasts[forecasts['trend_status'] == 'Rising'].head(3)
    
    if not rising.empty:
        cols = st.columns(len(rising))
        for i, (_, row) in enumerate(rising.iterrows()):
            with cols[i]:
                st.metric(label=f"🔥 {row['keyword'].title()}", 
                          value=f"{row['forecasted_volume']} searches", 
                          delta=f"{row['recent_growth_rate']*100:.1f}% growth")
                st.caption(f"Topic: {row['topic']}")
    else:
        st.info("No rapidly rising trends detected at this time.")
        
    st.markdown("---")
    st.subheader("All Trend Forecasts (Simple Exponential Smoothing)")
    
    def color_status(val):
        color = 'green' if val == 'Rising' else 'red' if val == 'Declining' else 'orange'
        return f'color: {color}'
        
    st.dataframe(forecasts.style.applymap(color_status, subset=['trend_status']))
    
    st.markdown("---")
    st.subheader("Historical Trend Search Volume")
    
    fig = px.line(df_trends, x='date', y='search_volume', color='keyword', 
                  title="Search Volume Over Time (Past 30 Days)")
    st.plotly_chart(fig, use_container_width=True)
