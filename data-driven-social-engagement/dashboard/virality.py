import streamlit as st
import plotly.express as px
import os
import joblib

def render_virality_prediction(df):
    st.title("Virality Prediction")
    
    if df is None or df.empty:
        st.warning("No data available.")
        return
        
    st.markdown("### Viral Coefficient Distribution")
    fig = px.histogram(df, x='viral_coefficient', nbins=30, 
                       title="Distribution of Viral Coefficients across all Content",
                       color_discrete_sequence=['#8A2BE2'])
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("Based on the **Viral Coefficient**, content is grouped into **LOW**, **MEDIUM**, and **HIGH** viral potential. ")
    st.info("💡 **Methodology**: The model predicts viral potential using ONLY pre-publication characteristics (topic, format, hook, etc.). The target labels (LOW/MEDIUM/HIGH) are derived from observed post-publication performance (Viral Coefficient). This strictly prevents data leakage while allowing us to predict future performance.")
    
    if 'viral_potential' in df.columns:
        pot_counts = df['viral_potential'].value_counts().reset_index()
        pot_counts.columns = ['Potential', 'Count']
        fig2 = px.pie(pot_counts, values='Count', names='Potential', 
                      title="Proportion of Viral Potential Categories",
                      color='Potential', 
                      color_discrete_map={'HIGH': '#00CC96', 'MEDIUM': '#FFA15A', 'LOW': '#EF553B'})
        st.plotly_chart(fig2, use_container_width=True)
        
    st.markdown("---")
    st.markdown("### Feature Importance (Machine Learning Model)")
    st.markdown("What pre-publication characteristics actually drive virality? (Data Leakage explicitly prevented by excluding engagement metrics from the prediction model).")
    
    # Try to load model metrics if available, otherwise just use mock layout
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(BASE_DIR, 'models', 'saved_models', 'viral_rf_model.pkl')
    
    try:
        from models.viral_prediction import ViralityPredictor
        vp = ViralityPredictor()
        metrics = vp.train_and_evaluate(df)
        
        if metrics and 'feature_importance' in metrics:
            import pandas as pd
            fi_df = pd.DataFrame(metrics['feature_importance'])
            fig3 = px.bar(fi_df, x='Importance', y='Feature', orientation='h',
                          title="Random Forest Feature Importance",
                          color='Importance', color_continuous_scale='Blues')
            fig3.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig3, use_container_width=True)
            
    except Exception as e:
        st.info("Train the model first to see Feature Importance.")
        st.code(str(e))
        
    st.markdown("---")
    st.subheader("Top 5 Viral Content Pieces")
    top_viral = df.sort_values(by='viral_coefficient', ascending=False).head(5)
    st.dataframe(top_viral[['title', 'topic', 'format', 'viral_coefficient', 'shares', 'saves', 'views']])
