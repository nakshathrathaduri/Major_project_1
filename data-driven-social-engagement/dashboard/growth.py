import streamlit as st
import plotly.express as px
import pandas as pd

def render_growth(df):
    st.title("Growth Dashboard")
    
    if df is None or df.empty:
        st.warning("No data available.")
        return
        
    st.markdown("### Follower Growth Impact")
    
    df['growth_absolute'] = df['followers_after'] - df['followers_before']
    df['growth_pct'] = (df['growth_absolute'] / df['followers_before']) * 100
    
    # Growth by topic
    topic_growth = df.groupby('topic')['growth_absolute'].mean().reset_index().sort_values('growth_absolute', ascending=False)
    
    fig1 = px.bar(topic_growth, x='topic', y='growth_absolute', 
                  title="Average Follower Growth by Topic",
                  color='growth_absolute', color_continuous_scale='Greens')
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("---")
    
    # Scatter plot to show what drives growth
    st.markdown("### Drivers of Growth")
    
    fig2 = px.scatter(df, x='shares', y='growth_pct', color='topic', size='views',
                      hover_data=['title'], title="Shares vs Follower Growth % (Size = Views)")
    st.plotly_chart(fig2, use_container_width=True)
    
    fig3 = px.scatter(df, x='saves', y='growth_pct', color='topic', size='views',
                      hover_data=['title'], title="Saves vs Follower Growth % (Size = Views)")
    st.plotly_chart(fig3, use_container_width=True)
