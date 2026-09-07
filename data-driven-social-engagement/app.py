import streamlit as st
import pandas as pd
import os

from ingestion.data_loader import load_data_from_csv
from preprocessing.preprocessing import clean_content_data, clean_comments_data, clean_trends_data
from analytics.virality import calculate_viral_coefficient, calculate_rates
from models.sentiment_model import analyze_comments

# Page config
st.set_page_config(
    page_title="Data-Driven Social Engagement",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data Source Selection
st.sidebar.title("Data Source")
data_source = st.sidebar.radio("Select Dataset:", ["Demo Dataset", "Uploaded Dataset"])

# Load data with caching
@st.cache_data
def get_processed_data(source):
    if source == "Demo Dataset":
        df_content_raw, df_comments_raw, df_trends_raw = load_data_from_csv()
    else:
        df_content_raw, df_comments_raw, df_trends_raw = load_data_from_csv(
            "uploaded_content.csv", "uploaded_comments.csv", "uploaded_trends.csv"
        )
    
    if df_content_raw is None:
        return None, None, None
        
    df_content = clean_content_data(df_content_raw)
    df_comments = clean_comments_data(df_comments_raw)
    df_trends = clean_trends_data(df_trends_raw)
    
    df_content = calculate_viral_coefficient(df_content)
    df_content = calculate_rates(df_content)
    
    if df_comments is not None and not df_comments.empty:
        # Avoid running heavy NLP on every load, but for demo we run it if it hasn't been saved
        if 'relatability_label' not in df_comments.columns:
            df_comments = analyze_comments(df_comments)
            
    return df_content, df_comments, df_trends

# Load the data
df_content, df_comments, df_trends = get_processed_data(data_source)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Module:", [
    "Home / Overview",
    "System Health / Validation",
    "Content Performance",
    "Virality Methodology",
    "Virality Prediction",
    "Sentiment & Relatability",
    "A/B Testing",
    "Recommendations",
    "Growth Dashboard",
    "Trend Forecasting",
    "Data Upload",
    "Model Performance",
    "Strategy Report",
    "About / Methodology"
])

# Global Filters
st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

filtered_content = df_content
if df_content is not None and not df_content.empty:
    platforms = ["All"] + sorted(list(df_content['platform'].dropna().unique()))
    topics = ["All"] + sorted(list(df_content['topic'].dropna().unique()))
    content_types = ["All"] + sorted(list(df_content['content_type'].dropna().unique()))
    formats = ["All"] + sorted(list(df_content['format'].dropna().unique()))
    hooks = ["All"] + sorted(list(df_content['hook_type'].dropna().unique()))
    segments = ["All"] + sorted(list(df_content['audience_segment'].dropna().unique()))
    
    selected_platform = st.sidebar.selectbox("Platform", platforms)
    selected_topic = st.sidebar.selectbox("Topic", topics)
    selected_type = st.sidebar.selectbox("Content Type", content_types)
    selected_format = st.sidebar.selectbox("Format", formats)
    selected_hook = st.sidebar.selectbox("Hook Type", hooks)
    selected_segment = st.sidebar.selectbox("Audience Segment", segments)
    
    if selected_platform != "All":
        filtered_content = filtered_content[filtered_content['platform'] == selected_platform]
    if selected_topic != "All":
        filtered_content = filtered_content[filtered_content['topic'] == selected_topic]
    if selected_type != "All":
        filtered_content = filtered_content[filtered_content['content_type'] == selected_type]
    if selected_format != "All":
        filtered_content = filtered_content[filtered_content['format'] == selected_format]
    if selected_hook != "All":
        filtered_content = filtered_content[filtered_content['hook_type'] == selected_hook]
    if selected_segment != "All":
        filtered_content = filtered_content[filtered_content['audience_segment'] == selected_segment]
    # Date Range Filter
    min_date = pd.to_datetime(df_content['content_date']).min().date()
    max_date = pd.to_datetime(df_content['content_date']).max().date()
    
    st.sidebar.markdown("---")
    date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_content = filtered_content[
            (pd.to_datetime(filtered_content['content_date']).dt.date >= start_date) & 
            (pd.to_datetime(filtered_content['content_date']).dt.date <= end_date)
        ]

# Router
if df_content is None and page not in ["Home / Overview", "About / Methodology"]:
    st.error("Dataset not found. Please ensure demo data is generated or upload CSVs.")
else:
    if page == "Home / Overview":
        from dashboard.overview import render_overview
        render_overview(filtered_content)
        
    elif page == "System Health / Validation":
        from dashboard.system_health import render_system_health
        render_system_health(df_content, df_comments, df_trends)
        
    elif page == "Content Performance":
        from dashboard.content import render_content_performance
        render_content_performance(filtered_content)
        
    elif page == "Virality Methodology":
        from dashboard.virality_methodology import render_virality_methodology
        render_virality_methodology()
        
    elif page == "Virality Prediction":
        from dashboard.virality import render_virality_prediction
        render_virality_prediction(filtered_content)
        
    elif page == "Sentiment & Relatability":
        from dashboard.sentiment import render_sentiment
        render_sentiment(df_comments, filtered_content)
        
    elif page == "A/B Testing":
        from dashboard.ab_testing import render_ab_testing
        render_ab_testing(filtered_content)
        
    elif page == "Recommendations":
        from dashboard.recommendations import render_recommendations
        render_recommendations(filtered_content)
        
    elif page == "Growth Dashboard":
        from dashboard.growth import render_growth
        render_growth(filtered_content)
        
    elif page == "Trend Forecasting":
        from dashboard.trends import render_trends
        render_trends(df_trends)
        
    elif page == "Data Upload":
        from dashboard.data_upload import render_data_upload
        render_data_upload()
        
    elif page == "Model Performance":
        from dashboard.model_performance import render_model_performance
        render_model_performance(filtered_content, df_comments)
        
    elif page == "Strategy Report":
        from dashboard.report import render_report
        render_report(filtered_content, df_comments, df_trends)
        
    elif page == "About / Methodology":
        from dashboard.about import render_about
        render_about()
