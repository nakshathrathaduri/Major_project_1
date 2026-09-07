import streamlit as st
import plotly.express as px
import pandas as pd

def render_sentiment(df_comments, df_content):
    st.title("Audience Sentiment & Relatability")
    
    if df_comments is None or df_comments.empty or 'relatability_label' not in df_comments.columns:
        st.warning("NLP Analysis has not been run on comments yet. Please wait or ensure spaCy/TextBlob is installed.")
        return
        
    st.markdown("### Comment NLP Analysis")
    st.markdown("This module processes comments to understand audience reactions. NLTK is used for text processing (tokenization), TextBlob is used to classify polarity (positive/negative sentiment), and spaCy assists in extracting relatability/problem themes by identifying linguistic triggers.")    
    col1, col2 = st.columns(2)
    
    with col1:
        sentiment_counts = df_comments['sentiment_label'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        fig1 = px.pie(sentiment_counts, values='Count', names='Sentiment', 
                      title="Sentiment Distribution",
                      color='Sentiment',
                      color_discrete_map={'Positive': '#00CC96', 'Neutral': '#636EFA', 'Negative': '#EF553B'})
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        rel_counts = df_comments['relatability_label'].value_counts().reset_index()
        rel_counts.columns = ['Relatability', 'Count']
        fig2 = px.pie(rel_counts, values='Count', names='Relatability', 
                      title="Relatability Distribution",
                      color='Relatability',
                      color_discrete_map={'Relatable': '#AB63FA', 'Neutral': '#B6E880'})
        st.plotly_chart(fig2, use_container_width=True)
        
    st.markdown("---")
    
    st.subheader("Topic vs Problem Awareness")
    st.markdown("Problem Awareness Score measures how deeply the audience relates to the problem (high relatability + negative/vulnerable sentiment).")
    
    # Merge comments with content to get topic
    merged = pd.merge(df_comments, df_content[['content_id', 'topic']], on='content_id', how='left')
    
    topic_awareness = merged.groupby('topic')['problem_awareness_score'].mean().reset_index().sort_values('problem_awareness_score', ascending=False)
    
    fig3 = px.bar(topic_awareness, x='topic', y='problem_awareness_score', 
                  title="Average Problem Awareness Score by Topic",
                  color='problem_awareness_score', color_continuous_scale='Magma')
    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    st.subheader("NLP Classification Examples")
    st.markdown("Why was a comment classified as relatable?")
    
    sample = df_comments[df_comments['relatability_label'] == 'Relatable'].head(10)
    st.dataframe(sample[['text', 'sentiment_label', 'relatability_label', 'relatability_score', 'relatability_explanation']])
