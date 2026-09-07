import streamlit as st

def render_about():
    st.title("About & Methodology")
    
    st.markdown("### The Data-Driven Social Engagement Initiative")
    st.markdown("This project serves as a Data Science Major Project designed to replace creative guesswork with evidence-based analytics.")
    
    st.markdown("---")
    
    st.subheader("1. Problem Statement")
    st.markdown("Content creators and marketers often rely on intuition to determine what content will perform well. While creativity is essential, the lack of quantifiable metrics regarding *why* content resonates (specifically regarding human struggles and relatability) leads to inconsistent engagement and unpredictable algorithmic reach.")
    
    st.subheader("2. Proposed Solution")
    st.markdown("We propose a unified Data Science pipeline that extracts engagement data, calculates a custom Viral Coefficient, predicts viral potential using machine learning, analyzes audience sentiment and relatability using NLP, and provides data-driven prescriptive recommendations.")
    
    st.subheader("3. Core Methodology")
    
    st.markdown("#### Feature Engineering & Viral Coefficient")
    st.markdown("Traditional engagement rates treat all interactions equally. We engineered a `Viral Coefficient` that explicitly weights high-value actions (Shares = 5.0, Saves = 4.0) over passive actions (Likes = 1.0), and multiplies the score by Retention Rate and Follower Growth Rate. This provides a true mathematical representation of algorithmic virality.")
    
    st.markdown("#### Machine Learning (Virality Prediction)")
    st.markdown("We trained a **Random Forest Classifier** to predict Viral Potential (LOW, MEDIUM, HIGH). **Crucially**, to prevent *Data Leakage*, the model is trained *exclusively* on pre-publication features (Topic, Format, Hook, Time, CTA, etc.), completely excluding post-publication engagement metrics from the feature set.")
    
    st.markdown("#### NLP (Sentiment & Relatability)")
    st.markdown("Using `TextBlob` and `spaCy`, the system analyzes comments. Instead of just basic sentiment, we implemented a custom linguistic trigger analysis to classify comments as **Relatable** vs **Neutral**, identifying expressions of personal recognition (e.g., 'I thought I was the only one'). Combined with negative sentiment, this generates a **Problem Awareness Score**.")
    
    st.markdown("#### Statistical Rigor (A/B Testing)")
    st.markdown("We do not rely on simple averages to determine winners. The system uses **Welch's t-test** for continuous bounded metrics (like retention) and the **Mann-Whitney U test** for highly skewed social media engagement metrics to calculate true statistical significance and p-values.")
    
    st.subheader("4. Limitations")
    st.markdown("""
    * **Platform API Constraints**: Real API access often restricts detailed data (like saves or retention) due to privacy. The architecture is built to support this when available via OAuth.
    * **NLP Context**: Sarcasm and heavy slang can still fool standard semantic models.
    * **Causation vs Correlation**: While we predict virality, the model identifies correlations. True causation in social media requires continuous controlled randomized experiments.
    """)
    
    st.subheader("5. Future Scope")
    st.markdown("""
    * Integration of Deep Learning (e.g., transformers like BERT) for more nuanced relatable-comment classification.
    * Live streaming API integrations for real-time dashboard updates.
    * Computer Vision to analyze the actual video frames for hook effectiveness.
    """)
