import streamlit as st
from recommender.strategy_recommender import generate_recommendations

def render_recommendations(df):
    st.title("Strategy Recommendations")
    
    if df is None or df.empty:
        st.warning("No data available.")
        return
        
    st.markdown("The recommender creates candidate strategies from values observed in the historical data and ranks them using the trained virality model when available. These recommendations are estimates based on historical patterns and do not guarantee performance.")
    
    recs = generate_recommendations(df, target_metric='viral_coefficient')
    
    if not recs:
        st.error("Could not generate recommendations.")
        return
        
    st.markdown("---")
    st.subheader("Top 5 Candidate Strategies (Ranked by ML Predicted Potential)")
    
    strategies = recs.get('top_strategies', [])
    if not strategies:
        st.error("No strategies generated.")
        return
        
    for i, strat in enumerate(strategies):
        with st.expander(f"🏆 Rank {i+1}: Topic '{strat['best_topic']['value']}' with '{strat['best_format']['value']}' (Score: {strat['expected_metric']['value']:.2f})", expanded=(i==0)):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**Topic:** {strat['best_topic']['value']}\n\n*{strat['best_topic']['evidence']}*")
                st.success(f"**Format:** {strat['best_format']['value']}\n\n*{strat['best_format']['evidence']}*")
                st.warning(f"**Hook:** {strat['best_hook']['value']}\n\n*{strat['best_hook']['evidence']}*")
                st.markdown(f"**Platform:** {strat.get('platform', 'N/A')}")
            with col2:
                st.info(f"**Posting Time:** {strat['best_time']['value']}\n\n*{strat['best_time']['evidence']}*")
                st.success(f"**CTA:** {strat['best_cta']['value']}\n\n*{strat['best_cta']['evidence']}*")
                st.markdown(f"**Content Type:** {strat.get('content_type', 'N/A')}")
                st.markdown(f"**Video Length:** {strat.get('video_length', 'N/A')}")
            with col3:
                st.markdown(f"**Caption Style:** {strat.get('caption_style', 'N/A')}")
                st.markdown(f"**Hashtags:** {strat.get('hashtag_count', 'N/A')}")
                st.markdown(f"**Audience Segment:** {strat.get('audience_segment', 'N/A')}")
                st.markdown("### 🚀 ML Evaluation")
                st.metric("Expected Potential Score", f"{strat['expected_metric']['value']:.2f}")
                st.caption(strat['expected_metric']['evidence'])
