import os
import pandas as pd
from database.database import SessionLocal, engine
from database.models import ContentPerformance, Comment, Trend

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_data_from_csv(content_csv="content_performance.csv", comments_csv="comments.csv", trends_csv="trends.csv"):
    """
    Loads data from CSV files.
    """
    try:
        df_content = pd.read_csv(os.path.join(DATA_DIR, content_csv))
        df_comments = pd.read_csv(os.path.join(DATA_DIR, comments_csv))
        df_trends = pd.read_csv(os.path.join(DATA_DIR, trends_csv))
        return df_content, df_comments, df_trends
    except FileNotFoundError:
        return None, None, None

def populate_database(df_content, df_comments, df_trends):
    """
    Populates the SQLite database from DataFrames.
    Uses append to preserve SQLAlchemy schemas, clearing existing data first.
    """
    if df_content is None:
        return
        
    # Clear existing data to avoid duplicates but keep schema intact
    with SessionLocal() as session:
        session.query(ContentPerformance).delete()
        session.query(Comment).delete()
        session.query(Trend).delete()
        session.commit()
    
    df_content.to_sql("content_performance", con=engine, if_exists="append", index=False)
    df_comments.to_sql("comments", con=engine, if_exists="append", index=False)
    df_trends.to_sql("trends", con=engine, if_exists="append", index=False)

def get_data_from_db():
    """
    Loads data from the SQLite database into pandas DataFrames.
    """
    try:
        df_content = pd.read_sql("SELECT * FROM content_performance", con=engine)
        df_comments = pd.read_sql("SELECT * FROM comments", con=engine)
        df_trends = pd.read_sql("SELECT * FROM trends", con=engine)
        return df_content, df_comments, df_trends
    except Exception as e:
        print(f"Error loading from DB: {e}")
        return None, None, None
