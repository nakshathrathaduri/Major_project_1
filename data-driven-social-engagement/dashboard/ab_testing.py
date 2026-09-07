import streamlit as st
import pandas as pd
from experiments.ab_testing import run_ab_test
import plotly.graph_objects as go

def render_ab_testing(df):
    st.title("A/B Testing")
    st.markdown("Run statistical A/B tests on historical data to compare different strategies.")
    
    if df is None or df.empty:
        st.warning("No data available.")
        return
        
    st.sidebar.markdown("---")
    st.sidebar.subheader("Experiment Configuration")
    
    # Define explicitly tested variables
    test_variables = ['format', 'hook_type', 'posting_time']
    metrics = ['engagement_rate', 'shares', 'saves', 'retention_rate', 'viral_coefficient', 'followers_after']
    
    variable = st.sidebar.selectbox("Test Variable", test_variables)
    
    unique_vals = list(df[variable].unique())
    if len(unique_vals) < 2:
        st.warning(f"Not enough unique values in {variable} to run a test.")
        return
        
    control = st.sidebar.selectbox("Control Group", unique_vals, index=0)
    treatment = st.sidebar.selectbox("Treatment Group", [v for v in unique_vals if v != control], index=0)
    
    metric = st.sidebar.selectbox("Target Metric", metrics)
    
    if st.sidebar.button("Run A/B Test"):
        with st.spinner("Running statistical tests..."):
            result = run_ab_test(df, variable, control, treatment, metric)
            
            if 'error' in result:
                st.error(result['error'])
            else:
                st.subheader(f"Experiment Results: {control} vs {treatment}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Control Mean", f"{result['mean_control']:.4f}")
                col2.metric("Treatment Mean", f"{result['mean_treatment']:.4f}")
                col3.metric("Improvement", f"{result['percentage_improvement']:.2f}%", 
                            f"{result['absolute_difference']:.4f} absolute")
                
                st.markdown("---")
                
                sig_color = "green" if result['statistically_significant'] else "red"
                sig_text = "YES" if result['statistically_significant'] else "NO"
                
                st.markdown(f"### Statistically Significant: <span style='color:{sig_color}'>{sig_text}</span>", unsafe_allow_html=True)
                
                st.markdown(f"**P-Value**: `{result['p_value']:.5f}` (Test used: {result['test_used']})")
                st.markdown(f"**95% Confidence Interval for Difference**: `[{result['ci_lower']:.4f}, {result['ci_upper']:.4f}]`")
                st.markdown(f"**Winner**: `{result['winner']}`")
                
                # Plot
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name=control,
                    x=[metric], y=[result['mean_control']],
                    error_y=dict(type='data', array=[result['ci_control_margin']])
                ))
                fig.add_trace(go.Bar(
                    name=treatment,
                    x=[metric], y=[result['mean_treatment']],
                    error_y=dict(type='data', array=[result['ci_treatment_margin']])
                ))
                fig.update_layout(barmode='group', title=f"Comparison of Means for {metric}")
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("💡 **Explanation**: If the p-value is less than 0.05, we conclude that the difference between the groups is statistically significant, meaning it is unlikely to have occurred by chance. The appropriate statistical test is chosen automatically: Welch's t-test for normally distributed continuous data, Mann-Whitney U for skewed engagement metrics, and Chi-square for categorical data.")
