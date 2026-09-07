import re
import spacy
from textblob import TextBlob
from nltk.tokenize import word_tokenize

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

def detect_relatability(text, sentiment_score=0.0):
    """
    Detects if a comment is relatable based on linguistic triggers, pronouns, and sentiment.
    Returns: (label, relatability_score, problem_awareness_score, explanation)
    """
    if not text:
        return "Neutral", 0.0, 0.0, "Empty comment"
        
    # Use a basic clean for exact phrase matching
    cleaned_basic = str(text).lower()
    cleaned_basic = re.sub(r'[^a-z0-9\s]', '', cleaned_basic).strip()
    
    # 1. Linguistic Triggers indicating personal experience/resonance
    strong_triggers = [
        "exactly me", "literally me", "same here", "i feel", "i struggle", 
        "i thought i was the only one", "happens to me", "my situation",
        "been through this", "i relate", "so true", "that is so me"
    ]
    
    weak_triggers = ["me too", "agree", "yes", "this", "fr", "facts"]
    
    score = 0.0
    explanations = []
    
    for trigger in strong_triggers:
        if trigger in cleaned_basic:
            score += 0.6
            explanations.append(f"Contains strong trigger: '{trigger}'")
            
    for trigger in weak_triggers:
        if trigger in cleaned_basic.split():
            score += 0.3
            explanations.append(f"Contains weak trigger: '{trigger}'")
            
    # 2. Pronoun usage and spaCy linguistic processing
    first_person = 0
    if nlp:
        doc = nlp(text)
        first_person = sum(1 for token in doc if token.text.lower() in ['i', 'me', 'my', 'mine', 'myself'])
        
        # Check for psychological/personal verbs (e.g., feel, think, struggle)
        personal_verbs = sum(1 for token in doc if token.pos_ == 'VERB' and token.lemma_ in ['feel', 'think', 'know', 'believe', 'struggle', 'try'])
        if personal_verbs > 0 and first_person > 0:
            score += 0.3
            explanations.append(f"Uses personal verbs with first-person context")
            
    else:
        # Fallback if spacy model isn't downloaded
        try:
            words = word_tokenize(cleaned_basic)
        except LookupError:
            # Fallback if NLTK punkt is not available
            words = cleaned_basic.split()
        
        first_person = sum(1 for w in words if w in ['i', 'me', 'my', 'mine', 'myself'])
        
    if first_person > 0:
        score += 0.2
        explanations.append(f"Uses first-person pronouns ({first_person} times)")
        
    # 3. Sentiment Integration
    # If the user expresses strong emotion (positive or negative) about their own situation, it's more likely relatable.
    if abs(sentiment_score) > 0.3 and first_person > 0:
        score += 0.2
        explanations.append(f"Combines strong sentiment with personal context")
            
    # Decision
    score = min(1.0, score)
    label = "Relatable" if score >= 0.5 else "Neutral"
    
    if score < 0.5:
        explanations = ["Lacks sufficient linguistic triggers for relatability"]
        
    explanation_text = "; ".join(explanations)
    
    # Calculate problem awareness based on negative sentiment + relatable
    # e.g., if someone relates to a struggle (negative sentiment), they are problem aware.
    problem_awareness = score * 1.5 if sentiment_score < 0 else score
    problem_awareness = min(1.0, problem_awareness)
    
    return label, score, problem_awareness, explanation_text
