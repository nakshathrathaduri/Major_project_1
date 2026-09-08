# major_project1
The Data-Driven Social Engagement Initiative
An evidence-based project for analyzing social media content performance, audience sentiment, virality, and growth.

1. Project Overview
This Data Science Major Project applies data analysis to social media strategy. It automatically processes content performance data, evaluates audience sentiment, calculates custom virality metrics, runs statistical A/B tests, and dynamically generates actionable strategy recommendations.

2. Seven Core Modules
Content Performance Tracker: Ingests, cleans, and structures performance metrics.
Virality Prediction Engine: Random Forest ML model predicting viral potential using only pre-publication features to prevent data leakage.
Audience Sentiment Analyzer: NLP module utilizing NLTK/TextBlob and spaCy to classify sentiment and detect relatability via linguistic triggers.
A/B Testing Framework: Statistical validation using Welch's t-test and Mann-Whitney U to identify statistically significant strategic advantages.
Engagement Optimization Recommender: Data-driven prescriptive analytics generating content strategy recommendations.
Growth Visualization Dashboard: An interactive Streamlit frontend with Plotly charts.
Trend Forecasting Module: Time-series exponential smoothing to detect emerging relatable struggles.
3. Installation & Setup
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment (Windows)
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Setup spaCy for NLP
python -m spacy download en_core_web_sm

# 5. Run tests
pytest -q

# 6. Run the application
streamlit run app.py
4. How to Use
Upon launching, the application automatically uses the Demo/Synthetic Dataset Mode. It will dynamically generate a highly realistic dataset of 800+ records (if not already generated) to demonstrate functionality without requiring API credentials. You can also upload your own datasets via the "Data Upload" module.
Navigate through the left sidebar to explore the Content Performance, A/B Testing, Machine Learning, and NLP pages.
Download the dynamically generated Strategy Report (Markdown or PDF) from the Strategy Report page.
5. Methodology & Rigor
No Data Leakage: The Virality Prediction ML model strictly excludes outcome metrics (likes, shares, views) from training features.
Statistical Significance: A/B testing accurately reports p-values and confidence intervals, explicitly stating when results lack statistical significance.
Custom Viral Coefficient: A mathematical formula weighing high-value network actions (Shares, Saves) far above passive vanity metrics (Likes).
Developed as a Major Project for Data Science & Engineering.
