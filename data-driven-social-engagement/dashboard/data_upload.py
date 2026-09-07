import streamlit as st
import pandas as pd
from ingestion.data_loader import populate_database

def render_data_upload():
    st.title("Data Upload & Management")
    st.markdown("Upload new CSV datasets to replace the current database for analysis.")
    
    st.info("Uploaded datasets are kept separate from the original demo dataset. The original demo files are not modified unless the user explicitly chooses to replace the current dataset.")
    
    st.markdown("### 1. Upload Content Performance Data")
    st.markdown("Required columns: `content_id`, `platform`, `content_date`, `topic`, `title`, `caption`, `content_type`, `format`, `hook_type`, `video_length`, `posting_time`, `views`, `likes`, `comments`, `shares`, `saves`, `followers_before`, `followers_after`, `retention_rate`, `hashtag_count`, `hashtags`, `cta_type`, `caption_style`, `audience_segment`")
    content_file = st.file_uploader("Upload Content CSV", type="csv", key="content")
    
    st.markdown("### 2. Upload Comments Data")
    st.markdown("Required columns: `comment_id`, `content_id`, `text`, `timestamp`")
    comments_file = st.file_uploader("Upload Comments CSV", type="csv", key="comments")
    
    st.markdown("### 3. Upload Trends Data")
    st.markdown("Required columns: `date`, `keyword`, `hashtag`, `topic`, `search_volume`, `mentions`, `growth_rate`")
    trends_file = st.file_uploader("Upload Trends CSV", type="csv", key="trends")
    
    if st.button("Process & Save as Uploaded Dataset"):
        if not (content_file and comments_file and trends_file):
            st.error("Please upload all three required CSV files.")
            return
            
        try:
            df_content = pd.read_csv(content_file)
            df_comments = pd.read_csv(comments_file)
            df_trends = pd.read_csv(trends_file)
            
            # Validation Schemas
            content_req = ['content_id', 'platform', 'content_date', 'topic', 'title', 'caption', 'content_type', 'format', 'hook_type', 'video_length', 'posting_time', 'views', 'likes', 'comments', 'shares', 'saves', 'followers_before', 'followers_after', 'retention_rate', 'hashtag_count', 'hashtags', 'cta_type', 'caption_style', 'audience_segment']
            comments_req = ['comment_id', 'content_id', 'text', 'timestamp']
            trends_req = ['date', 'keyword', 'hashtag', 'topic', 'search_volume', 'mentions', 'growth_rate']
            
            def validate_df(df, req_cols, name):
                missing = [c for c in req_cols if c not in df.columns]
                if missing:
                    st.error(f"Validation Error in {name} CSV: Missing columns: {', '.join(missing)}")
                    return False
                return True
                
            v1 = validate_df(df_content, content_req, "Content")
            v2 = validate_df(df_comments, comments_req, "Comments")
            v3 = validate_df(df_trends, trends_req, "Trends")
            
            if not (v1 and v2 and v3):
                return
                
            st.success("Validation Passed: All required columns present.")
            
            with st.expander("Preview Validated Data"):
                st.write("Content Preview", df_content.head(2))
                st.write("Comments Preview", df_comments.head(2))
                st.write("Trends Preview", df_trends.head(2))
            
            import os
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            DATA_DIR = os.path.join(BASE_DIR, 'data')
            
            # Save to separate uploaded files
            df_content.to_csv(os.path.join(DATA_DIR, "uploaded_content.csv"), index=False)
            df_comments.to_csv(os.path.join(DATA_DIR, "uploaded_comments.csv"), index=False)
            df_trends.to_csv(os.path.join(DATA_DIR, "uploaded_trends.csv"), index=False)
            
            st.success(f"✅ Successfully saved {len(df_content)} content records, {len(df_comments)} comments, and {len(df_trends)} trend records as the Uploaded Dataset.")
            st.info("You can now select 'Uploaded Dataset' from the sidebar to use this data across all modules.")
            
        except Exception as e:
            st.error(f"Error processing upload: {e}")
