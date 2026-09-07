from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from database.database import Base

class ContentPerformance(Base):
    __tablename__ = "content_performance"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(String, unique=True, index=True)
    platform = Column(String)
    content_date = Column(DateTime)
    topic = Column(String, index=True)
    title = Column(String)
    caption = Column(String)
    content_type = Column(String)
    format = Column(String)
    hook_type = Column(String)
    video_length = Column(Float)
    posting_time = Column(String)
    
    # Engagement Metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    
    # Growth & Retention
    followers_before = Column(Integer, default=0)
    followers_after = Column(Integer, default=0)
    retention_rate = Column(Float, default=0.0)
    
    # Metadata
    hashtag_count = Column(Integer, default=0)
    hashtags = Column(String)
    cta_type = Column(String)
    caption_style = Column(String)
    audience_segment = Column(String)
    
    # Derived Metrics (Calculated later)
    viral_coefficient = Column(Float, nullable=True)
    viral_potential = Column(String, nullable=True)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(String, unique=True, index=True)
    content_id = Column(String, ForeignKey("content_performance.content_id"))
    text = Column(String)
    timestamp = Column(DateTime, default=func.now())
    
    # NLP Outputs
    sentiment_label = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    relatability_label = Column(String, nullable=True)
    relatability_score = Column(Float, nullable=True)
    problem_awareness_score = Column(Float, nullable=True)

class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    keyword = Column(String, index=True)
    hashtag = Column(String)
    topic = Column(String)
    search_volume = Column(Integer)
    mentions = Column(Integer)
    growth_rate = Column(Float)
    trend_status = Column(String) # Rising, Stable, Declining
