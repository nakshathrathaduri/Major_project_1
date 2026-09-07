import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_content_performance(df):
    st.title("Content Performance Dashboard")
    
    if df is None or df.empty:
        st.warning("No data available.")
        return
        
    st.markdown("### Engagement Over Time")
    df['content_date'] = pd.to_datetime(df['content_date'])
    df_sorted = df.sort_values('content_date')
    
    # Engagement metrics line chart
    fig1 = px.line(df_sorted, x='content_date', y=['views', 'likes', 'comments'], 
                   title="Core Engagement Metrics Over Time")
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("### High-Value Actions (Saves & Shares)")
    fig2 = px.line(df_sorted, x='content_date', y=['shares', 'saves'], 
                   title="Saves and Shares Over Time", color_discrete_sequence=['#FF9900', '#00CC96'])
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Save-to-Share Ratio Analysis")
    st.markdown("The Save-to-Share ratio identifies content that resonates deeply (Saves) vs content designed for social validation (Shares).")
    
    topic_sts = df.groupby('topic')['save_to_share_ratio'].mean().reset_index().sort_values('save_to_share_ratio', ascending=False)
    fig3 = px.bar(topic_sts, x='topic', y='save_to_share_ratio', title="Average Save-to-Share Ratio by Topic", color='save_to_share_ratio')
    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Retention Analysis")
    format_retention = df.groupby('format')['retention_rate'].mean().reset_index()
    fig4 = px.pie(format_retention, values='retention_rate', names='format', title="Average Retention Rate by Format")
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("### Correlation Matrix")
    numeric_df = df[['views', 'likes', 'comments', 'shares', 'saves', 'retention_rate', 'followers_after', 'viral_coefficient']]
    corr = numeric_df.corr()
    
    fig5 = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu_r',
        zmin=-1, zmax=1
    ))
    fig5.update_layout(title="Correlation Heatmap for Engagement Metrics")
    st.plotly_chart(fig5, use_container_width=True)
