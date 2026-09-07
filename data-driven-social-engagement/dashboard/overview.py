import streamlit as st
import plotly.express as px

def render_overview(df):
    st.title("The Data-Driven Social Engagement Initiative")
    st.markdown("### *Measure emotion. Quantify relatability. Optimize human connection.*")
    
    st.markdown("---")
    
    if df is None or df.empty:
        st.warning("No data available.")
        return
        
    st.subheader("Key Performance Indicators (KPIs)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Content", len(df))
        st.metric("Total Shares", f"{df['shares'].sum():,}")
    with col2:
        st.metric("Total Views", f"{df['views'].sum():,}")
        st.metric("Total Saves", f"{df['saves'].sum():,}")
    with col3:
        st.metric("Total Likes", f"{df['likes'].sum():,}")
        st.metric("Avg Retention", f"{df['retention_rate'].mean()*100:.1f}%")
    with col4:
        st.metric("Total Comments", f"{df['comments'].sum():,}")
        st.metric("Avg Viral Coef", f"{df['viral_coefficient'].mean():.2f}")
        
    st.markdown("---")
    
    st.subheader("At a Glance: Topic Performance")
    topic_perf = df.groupby('topic')[['views', 'engagement_rate', 'viral_coefficient']].mean().reset_index()
    
    fig = px.bar(topic_perf, x='topic', y='viral_coefficient', 
                 title="Average Viral Coefficient by Topic",
                 color='engagement_rate',
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### Project Modules
    The application brings the main analysis tasks into one Streamlit dashboard. It can track content performance, analyze comments, predict viral potential, compare A/B variants, generate recommendations, and forecast trends.
    
    1. **Content Performance**: Ingests and cleans social media data.
    2. **Virality Prediction**: Machine learning model to estimate viral potential based on historical patterns.
    3. **Sentiment Analysis**: NLP module to classify sentiment and detect relatability themes.
    4. **A/B Testing**: Statistical tests to compare content formats.
    5. **Recommendations**: Candidate strategies derived from historical top performers.
    6. **Trend Forecasting**: Time-series estimates for future topics.
    """)
