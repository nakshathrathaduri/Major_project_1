import pandas as pd
from textblob import TextBlob
import re
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if not downloaded
    nlp = None

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # NLTK: Tokenization and Stopword removal
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    # Keep some important words for relatability context
    stop_words.difference_update(['i', 'me', 'my', 'mine']) 
    filtered_tokens = [w for w in tokens if w not in stop_words]
    
    # spaCy: Lemmatization where practical
    if nlp:
        doc = nlp(" ".join(filtered_tokens))
        filtered_tokens = [token.lemma_ for token in doc]
        
    return " ".join(filtered_tokens).strip()

def get_sentiment(text):
    if not text:
        return "Neutral", 0.0
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    if score > 0.1:
        return "Positive", score
    elif score < -0.1:
        return "Negative", score
    else:
        return "Neutral", score

def analyze_comments(df_comments):
    """
    Processes a dataframe of comments and adds NLP analysis.
    """
    if df_comments is None or df_comments.empty:
        return df_comments
        
    from models.relatability import detect_relatability
        
    df = df_comments.copy()
    
    sentiments = []
    sentiment_scores = []
    relatability_labels = []
    relatability_scores = []
    problem_awareness_scores = []
    explanations = []
    
    for text in df['text']:
        s_label, s_score = get_sentiment(text)
        r_label, r_score, p_score, expl = detect_relatability(text, s_score)
        
        sentiments.append(s_label)
        sentiment_scores.append(s_score)
        relatability_labels.append(r_label)
        relatability_scores.append(r_score)
        problem_awareness_scores.append(p_score)
        explanations.append(expl)
        
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = sentiment_scores
    df['relatability_label'] = relatability_labels
    df['relatability_score'] = relatability_scores
    df['problem_awareness_score'] = problem_awareness_scores
    df['relatability_explanation'] = explanations
    
    return df
