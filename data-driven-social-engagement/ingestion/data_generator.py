import os
import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def generate_demo_data(num_records=800):
    """
    Generates realistic synthetic data for the Data-Driven Social Engagement Initiative.
    """
    np.random.seed(42)
    random.seed(42)
    
    topics = [
        "Social Anxiety", "Dating", "Career Pressure", "Academic Stress", 
        "Loneliness", "Self Confidence", "Overthinking", "Relationships", 
        "Productivity", "Financial Stress"
    ]
    
    formats = ["Short Video", "Long Video", "Carousel", "Single Image"]
    hook_types = ["Visual Hook", "Text Hook", "Audio Hook", "Question Hook", "Story Hook"]
    posting_times = ["Morning (8-11 AM)", "Afternoon (12-4 PM)", "Evening (5-8 PM)", "Night (9 PM-12 AM)"]
    cta_types = ["Share this", "Save for later", "Comment your thoughts", "Follow for more", "Link in bio", "None"]
    caption_styles = ["Emotion + Personal Story", "Educational / Tips", "Short & Punchy", "Question to Audience", "Long-form vulnerable"]
    audience_segments = ["Gen Z", "Millennials", "Professionals", "Students", "General"]
    platforms = ["Instagram", "YouTube", "TikTok"]

    # --- Generate Content Performance Data ---
    content_data = []
    
    start_date = datetime.now() - timedelta(days=180)
    
    for i in range(num_records):
        content_id = f"CONTENT_{uuid.uuid4().hex[:8].upper()}"
        topic = np.random.choice(topics, p=[0.15, 0.1, 0.1, 0.1, 0.15, 0.1, 0.15, 0.05, 0.05, 0.05])
        format_type = np.random.choice(formats, p=[0.5, 0.2, 0.2, 0.1])
        hook = np.random.choice(hook_types)
        posting_time = np.random.choice(posting_times)
        
        # Base multiplier based on topic "relatability"
        topic_multiplier = 1.0
        if topic in ["Social Anxiety", "Loneliness", "Overthinking"]:
            topic_multiplier = 1.5
            
        # Format multiplier
        format_multiplier = 1.0
        video_length = 0
        if format_type == "Short Video":
            format_multiplier = 1.3
            video_length = np.random.uniform(15, 60)
        elif format_type == "Long Video":
            format_multiplier = 0.8
            video_length = np.random.uniform(120, 600)
            
        # Hook multiplier
        hook_multiplier = 1.2 if hook in ["Visual Hook", "Story Hook"] else 1.0
        
        # Calculate base views
        base_views = int(np.random.lognormal(mean=9, sigma=1.5))
        views = int(base_views * topic_multiplier * format_multiplier * hook_multiplier)
        
        # Engagement metrics (realistic funnel)
        # Retention is higher for short videos and good hooks
        base_retention = np.random.uniform(0.1, 0.5)
        if format_type == "Short Video":
            base_retention += 0.2
        if hook in ["Visual Hook", "Story Hook"]:
            base_retention += 0.1
        retention_rate = min(0.95, base_retention)
        
        # Likes: ~5-15% of views
        likes = int(views * np.random.uniform(0.05, 0.15))
        
        # Comments: ~0.5-2% of views
        comments = int(views * np.random.uniform(0.005, 0.02))
        
        # Shares and Saves: Heavily influenced by topic and CTA
        cta = np.random.choice(cta_types)
        share_rate = np.random.uniform(0.001, 0.05)
        save_rate = np.random.uniform(0.001, 0.05)
        
        if topic_multiplier > 1.0: # Relatable topics
            share_rate *= 2.0
            save_rate *= 1.8
            
        if cta == "Share this":
            share_rate *= 1.5
        if cta == "Save for later":
            save_rate *= 1.5
            
        shares = int(views * share_rate)
        saves = int(views * save_rate)
        
        # Follower Growth
        followers_before = np.random.randint(1000, 50000)
        # Growth correlates with shares, saves and retention
        growth_factor = (shares * 2 + saves * 1.5 + retention_rate * views * 0.01) * np.random.uniform(0.05, 0.15)
        followers_after = followers_before + int(growth_factor)
        
        content_date = start_date + timedelta(days=np.random.randint(0, 180))
        
        content_data.append({
            "content_id": content_id,
            "platform": np.random.choice(platforms),
            "content_date": content_date.strftime("%Y-%m-%d %H:%M:%S"),
            "topic": topic,
            "title": f"The truth about {topic.lower()}",
            "caption": f"Let's talk about {topic.lower()}. #growth #mentalhealth",
            "content_type": "Organic",
            "format": format_type,
            "hook_type": hook,
            "video_length": round(video_length, 1),
            "posting_time": posting_time,
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "saves": saves,
            "followers_before": followers_before,
            "followers_after": followers_after,
            "retention_rate": round(retention_rate, 2),
            "hashtag_count": np.random.randint(1, 10),
            "hashtags": f"#{topic.replace(' ', '')} #struggle",
            "cta_type": cta,
            "caption_style": np.random.choice(caption_styles),
            "audience_segment": np.random.choice(audience_segments)
        })

    df_content = pd.DataFrame(content_data)
    df_content.to_csv(os.path.join(DATA_DIR, "content_performance.csv"), index=False)
    
    # --- Generate Comments Data ---
    comments_data = []
    
    relatable_phrases = [
        "I feel exactly the same way",
        "This happens to me all the time",
        "I thought I was the only one",
        "same here",
        "I've been through this",
        "this is literally me",
        "I struggle with this daily",
        "I can relate",
        "exactly my situation"
    ]
    
    neutral_phrases = [
        "Nice video",
        "Great tips",
        "Thanks for sharing",
        "Interesting perspective",
        "Good content",
        "Hello from Brazil",
        "I don't really agree but okay"
    ]
    
    for idx, row in df_content.iterrows():
        # Generate 1 to 5 comments per content for demo purposes
        num_comments = np.random.randint(1, 6)
        is_relatable_topic = row['topic'] in ["Social Anxiety", "Loneliness", "Overthinking"]
        
        for _ in range(num_comments):
            comment_id = f"COMM_{uuid.uuid4().hex[:8].upper()}"
            
            # If the topic is relatable, higher chance of a relatable comment
            if is_relatable_topic:
                text = np.random.choice(relatable_phrases, p=[0.15]*4 + [0.10]*4 + [0.00]*1) if np.random.rand() > 0.3 else np.random.choice(neutral_phrases)
            else:
                text = np.random.choice(neutral_phrases) if np.random.rand() > 0.2 else np.random.choice(relatable_phrases)
                
            comments_data.append({
                "comment_id": comment_id,
                "content_id": row['content_id'],
                "text": text,
                "timestamp": (datetime.strptime(row['content_date'], "%Y-%m-%d %H:%M:%S") + timedelta(hours=np.random.randint(1, 48))).strftime("%Y-%m-%d %H:%M:%S")
            })
            
    df_comments = pd.DataFrame(comments_data)
    df_comments.to_csv(os.path.join(DATA_DIR, "comments.csv"), index=False)
    
    # --- Generate Trends Data ---
    trends_data = []
    current_date = datetime.now()
    
    trend_keywords = {
        "Social Anxiety": ["social anxiety", "overwhelmed in public", "social battery"],
        "Academic Stress": ["study burnout", "exam pressure", "failing college"],
        "Dating": ["dating burnout", "ghosting", "dating apps exhaustion"],
        "Career Pressure": ["quiet quitting", "job market stress", "imposter syndrome"]
    }
    
    for topic, keywords in trend_keywords.items():
        for keyword in keywords:
            for day in range(30):
                date = current_date - timedelta(days=30-day)
                base_volume = np.random.randint(1000, 5000)
                # Add an upward trend to some keywords
                trend_factor = 1.0 + (day * 0.02) if "burnout" in keyword or "anxiety" in keyword else 1.0 + np.random.uniform(-0.1, 0.1)
                volume = int(base_volume * trend_factor)
                
                trends_data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "keyword": keyword,
                    "hashtag": f"#{keyword.replace(' ', '')}",
                    "topic": topic,
                    "search_volume": volume,
                    "mentions": int(volume * 0.1),
                    "growth_rate": round(trend_factor - 1.0, 3)
                })
                
    df_trends = pd.DataFrame(trends_data)
    df_trends.to_csv(os.path.join(DATA_DIR, "trends.csv"), index=False)
    
    print(f"Generated {len(df_content)} content records, {len(df_comments)} comments, and {len(df_trends)} trend records.")
    return df_content, df_comments, df_trends

if __name__ == "__main__":
    generate_demo_data()
