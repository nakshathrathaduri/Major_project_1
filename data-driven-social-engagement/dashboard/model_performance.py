import streamlit as st
import pandas as pd
import os

def render_model_performance(df_content, df_comments):
    st.title("Model Performance")
    
    st.markdown("### 1. Virality Prediction Model (Random Forest)")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(BASE_DIR, 'models', 'saved_models', 'viral_rf_model.pkl')
    
    st.markdown("This model predicts whether content will have LOW, MEDIUM, or HIGH viral potential based **strictly on pre-publication characteristics**. We deliberately exclude engagement metrics (likes, shares, views) from the input features to prevent data leakage, ensuring a valid predictive model.")
    
    if df_content is not None and not df_content.empty:
        try:
            from models.viral_prediction import ViralityPredictor
            vp = ViralityPredictor()
            # Retrain for demo purposes to show live metrics
            with st.spinner("Calculating live model metrics..."):
                metrics = vp.train_and_evaluate(df_content)
                
            if metrics:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Accuracy", f"{metrics['accuracy']:.2f}")
                col2.metric("Precision (Weighted)", f"{metrics['precision']:.2f}")
                col3.metric("Recall (Weighted)", f"{metrics['recall']:.2f}")
                col4.metric("F1-Score", f"{metrics['f1_score']:.2f}")
                
                st.markdown("#### Confusion Matrix")
                cm_df = pd.DataFrame(metrics['confusion_matrix'], 
                                     index=[f"True {c}" for c in metrics['classes']],
                                     columns=[f"Pred {c}" for c in metrics['classes']])
                st.dataframe(cm_df)
                
                st.markdown(f"**Training Samples**: {metrics['train_size']} | **Testing Samples**: {metrics['test_size']}")
                
        except Exception as e:
            st.error(f"Could not calculate model metrics: {e}")
    else:
        st.warning("Data not available to run model.")
        
    st.markdown("---")
    
    st.markdown("### 2. NLP Sentiment & Relatability Classifier")
    st.markdown("The NLP model uses linguistic trigger analysis and semantic processing (via spaCy and TextBlob) to classify text without relying entirely on hard-coded lists.")
    
    if df_comments is not None and 'relatability_label' in df_comments.columns:
        # Show sample classifications
        st.markdown("#### Sample Output Validations")
        
        # Get one of each
        sample_relatable = df_comments[df_comments['relatability_label'] == 'Relatable'].head(2)
        sample_neutral = df_comments[df_comments['relatability_label'] == 'Neutral'].head(2)
        
        combined = pd.concat([sample_relatable, sample_neutral])
        
        st.dataframe(combined[['text', 'sentiment_label', 'sentiment_score', 'relatability_label', 'relatability_score', 'problem_awareness_score']])
        
    else:
        st.info("NLP model has not processed the comments dataset yet.")
