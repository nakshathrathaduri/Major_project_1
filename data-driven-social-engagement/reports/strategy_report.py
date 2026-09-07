import os
from fpdf import FPDF
from recommender.strategy_recommender import generate_recommendations

def create_markdown_report(df_content, df_comments, df_trends):
    """
    Dynamically generates a Markdown Strategy Report based on data.
    """
    if df_content is None or df_content.empty:
        return "No data available to generate report."
        
    recommendations = generate_recommendations(df_content)
    
    top_strategies = recommendations.get('top_strategies', [])
    if top_strategies:
        best_strat = top_strategies[0]
        best_topic = best_strat.get('best_topic', {}).get('value', 'N/A')
        worst_topic = df_content.groupby('topic')['viral_coefficient'].mean().sort_values().index[0]
        
        avg_vc = df_content['viral_coefficient'].mean()
        
        report = f"""# The Data-Driven Social Engagement Initiative
## Final Strategy Report

**Generated dynamically from the latest dataset.**

### 1. Introduction
This report summarizes the findings of our Data Science Major Project. The goal is to analyze social media engagement using data-driven techniques.

### 2. Dataset
The analysis is based on historical social media performance data, including engagement metrics and audience comments.

### 3. Methodology
We apply data preprocessing, natural language processing (NLP), statistical A/B testing, and machine learning (Random Forest) to extract actionable insights.

### 4. Analysis & Model Results
* **Average Viral Coefficient:** {avg_vc:.2f}
* **Best Performing Topic:** {best_topic} ({best_strat.get('best_topic', {}).get('evidence', '')})
* **Lowest Performing Topic:** {worst_topic}
* **Expected Viral Potential (if using optimal strategy):** {best_strat.get('expected_metric', {}).get('value', 0):.2f}

### 5. Audience Sentiment
"""
        if df_comments is not None and 'relatability_label' in df_comments.columns:
            relatable_pct = (df_comments['relatability_label'] == 'Relatable').mean() * 100
            avg_prob_awareness = df_comments['problem_awareness_score'].mean()
            report += f"* **Relatable Comments:** {relatable_pct:.1f}%\n"
            report += f"* **Average Problem Awareness Score:** {avg_prob_awareness:.2f}\n"
        else:
            report += "NLP Data not processed yet.\n"
            
        report += f"""
### 6. Recommendations
Based on historical data and ML predictions, the model estimates the following content format will perform well:
* **Topic:** {best_topic}
* **Format:** {best_strat.get('best_format', {}).get('value', 'N/A')}
* **Hook:** {best_strat.get('best_hook', {}).get('value', 'N/A')}
* **Time:** {best_strat.get('best_time', {}).get('value', 'N/A')}
* **CTA:** {best_strat.get('best_cta', {}).get('value', 'N/A')}

### 7. Limitations
* The model assumes past performance is indicative of future algorithmic behavior.
* Predictions rely on accurate tracking of Saves and Shares.

### 8. Conclusion
By using a data-driven approach rather than guesswork, we can identify which content elements historically correlate with higher virality and relatability.
"""
    else:
        report = "Could not generate strategies."

    return report


