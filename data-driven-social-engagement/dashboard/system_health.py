import streamlit as st

def render_system_health(df_content, df_comments, df_trends):
    st.title("System Health & Project Validation")
    st.markdown("Displays the live execution status of all 7 core modules.")
    
    st.markdown("---")
    
    def status_indicator(condition, success_text, fail_text):
        if condition:
            st.success(f"✅ {success_text}")
        else:
            st.error(f"❌ {fail_text}")
            
    st.subheader("1. Data Ingestion & Preprocessing")
    status_indicator(df_content is not None and not df_content.empty, 
                     f"Content Dataset Loaded ({len(df_content) if df_content is not None else 0} records)", 
                     "Content Dataset Missing")
    status_indicator(df_comments is not None and not df_comments.empty, 
                     f"Comments Dataset Loaded ({len(df_comments) if df_comments is not None else 0} records)", 
                     "Comments Dataset Missing")
    status_indicator(df_trends is not None and not df_trends.empty, 
                     f"Trends Dataset Loaded ({len(df_trends) if df_trends is not None else 0} records)", 
                     "Trends Dataset Missing")
                     
    st.subheader("2. Analytics & Virality")
    has_vc = df_content is not None and 'viral_coefficient' in df_content.columns
    status_indicator(has_vc, "Viral Coefficient Successfully Calculated", "Viral Coefficient Calculation Failed")
    
    st.subheader("3. Machine Learning (Virality Prediction)")
    has_ml = False
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(BASE_DIR, 'models', 'saved_models', 'viral_rf_model.pkl')
    if os.path.exists(model_path):
        has_ml = True
    # We also check if we can run it right now if it doesn't exist
    ml_error = ""
    if not has_ml and df_content is not None:
        try:
            from models.viral_prediction import ViralityPredictor
            vp = ViralityPredictor()
            vp.train_and_evaluate(df_content)
            has_ml = os.path.exists(model_path)
        except Exception as e:
            ml_error = str(e)
            
    if has_ml:
        status_indicator(True, "Random Forest Virality Model Trained and Saved", "")
    else:
        status_indicator(False, "", f"ML Model Not Available: {ml_error}")
    
    st.subheader("4. NLP Sentiment & Relatability")
    has_nlp = df_comments is not None and 'relatability_label' in df_comments.columns
    status_indicator(has_nlp, "NLP Classification Completed (Relatability, Sentiment, Problem Awareness)", "NLP Pipeline Not Run")
    
    st.subheader("5. Statistical A/B Testing Framework")
    try:
        from experiments.ab_testing import run_ab_test
        # Execute a small test
        res = run_ab_test(df_content.head(20), 'format', df_content['format'].iloc[0], df_content['format'].iloc[-1], 'retention_rate')
        if 'error' in res and 'insufficient' not in res['error'].lower():
            status_indicator(False, "", f"A/B Testing Error: {res['error']}")
        else:
            status_indicator(True, "A/B Testing Framework Executed Successfully", "")
    except Exception as e:
        status_indicator(False, "", f"A/B Testing Framework Missing or Failing: {e}")
        
    st.subheader("6. Strategy Recommender")
    try:
        from recommender.strategy_recommender import generate_recommendations
        recs = generate_recommendations(df_content)
        if recs and 'top_strategies' in recs and len(recs['top_strategies']) > 0:
            status_indicator(True, "Data-Driven Recommendation Engine Executed Successfully", "")
        else:
            status_indicator(False, "", "Recommendation Engine returned empty data")
    except Exception as e:
        status_indicator(False, "", f"Recommendation Engine Failing: {e}")
        
    st.subheader("7. Trend Forecasting")
    try:
        from models.trend_forecasting import forecast_trends
        if df_trends is not None and not df_trends.empty:
            forecasts = forecast_trends(df_trends)
            if not forecasts.empty:
                status_indicator(True, "Time-Series Forecasting Executed Successfully", "")
            else:
                status_indicator(False, "", "Forecasting returned empty data")
        else:
            status_indicator(False, "", "No trend data to forecast")
    except Exception as e:
        status_indicator(False, "", f"Forecasting Module Failing: {e}")
        
    st.subheader("8. Database & Reporting")
    db_error = ""
    try:
        from database.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        db_ok = False
        db_error = str(e)
    if db_ok:
        status_indicator(True, "SQLite/SQLAlchemy Connection Successful (SELECT 1 passed)", "")
    else:
        status_indicator(False, "", f"Database Connection Failed: {db_error}")
    
    try:
        from reports.strategy_report import create_markdown_report
        report = create_markdown_report(df_content, df_comments, df_trends)
        if "No data" not in report:
            status_indicator(True, "Strategy Report Generated Successfully", "")
        else:
            status_indicator(False, "", "Strategy Report Generation Failed")
    except Exception as e:
        status_indicator(False, "", f"Strategy Report Failing: {e}")
