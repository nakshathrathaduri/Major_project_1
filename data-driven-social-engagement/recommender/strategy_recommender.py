import pandas as pd
import os
import joblib
import itertools

def generate_recommendations(df, target_metric='viral_coefficient'):
    """
    Generates data-driven recommendations based on the historical dataset.
    Uses trained ML model to score and rank MULTIPLE candidate strategies.
    Returns the TOP 5 strategies.
    """
    if df is None or df.empty or target_metric not in df.columns:
        return None
        
    # Historical Best Aggregations (used for evidence)
    topic_perf = df.groupby('topic')[target_metric].mean().sort_values(ascending=False)
    format_perf = df.groupby('format')[target_metric].mean().sort_values(ascending=False)
    hook_perf = df.groupby('hook_type')[target_metric].mean().sort_values(ascending=False)
    time_perf = df.groupby('posting_time')[target_metric].mean().sort_values(ascending=False)
    cta_perf = df.groupby('cta_type')[target_metric].mean().sort_values(ascending=False)
    
    # Extract top 2 performing categories for all dimensions
    top_topics = topic_perf.index[:2].tolist()
    top_formats = format_perf.index[:2].tolist()
    top_hooks = hook_perf.index[:2].tolist()
    top_times = time_perf.index[:2].tolist()
    top_ctas = cta_perf.index[:2].tolist()
    
    platform_perf = df.groupby('platform')[target_metric].mean().sort_values(ascending=False)
    ctype_perf = df.groupby('content_type')[target_metric].mean().sort_values(ascending=False)
    caption_perf = df.groupby('caption_style')[target_metric].mean().sort_values(ascending=False)
    audience_perf = df.groupby('audience_segment')[target_metric].mean().sort_values(ascending=False)
    
    top_platforms = platform_perf.index[:2].tolist()
    top_ctypes = ctype_perf.index[:2].tolist()
    top_captions = caption_perf.index[:2].tolist()
    top_audiences = audience_perf.index[:2].tolist()
    
    # Use realistic central tendencies for numerics
    c_video_length = df['video_length'].median()
    c_hashtag_count = df['hashtag_count'].median()
    
    # Generate bounded combinations (2^9 = 512 combinations, very fast for RF)
    combinations = list(itertools.product(
        top_topics, top_formats, top_hooks, top_times, top_ctas,
        top_platforms, top_ctypes, top_captions, top_audiences
    ))
    
    candidates = []
    for combo in combinations:
        candidates.append({
            'topic': combo[0],
            'format': combo[1],
            'hook_type': combo[2],
            'posting_time': combo[3],
            'cta_type': combo[4],
            'platform': combo[5],
            'content_type': combo[6],
            'caption_style': combo[7],
            'audience_segment': combo[8],
            'video_length': c_video_length,
            'hashtag_count': c_hashtag_count
        })
        
    candidates_df = pd.DataFrame(candidates)
    
    top_strategies = []
    
    # Try to use ML Model for expected potential
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(BASE_DIR, 'models', 'saved_models', 'viral_rf_model.pkl')
        pipeline = joblib.load(model_path)
        
        # Predict probability of being HIGH viral potential
        probs = pipeline.predict_proba(candidates_df)
        classes = pipeline.classes_
        if 'HIGH' in classes:
            high_idx = list(classes).index('HIGH')
            candidates_df['prob_high'] = probs[:, high_idx] * 100
            
            # Sort by highest probability
            ranked = candidates_df.sort_values(by='prob_high', ascending=False).head(5)
            
            for idx, row in ranked.iterrows():
                top_strategies.append({
                    'expected_metric': {'value': row['prob_high'], 'evidence': 'Random Forest predicted probability of HIGH virality'},
                    'best_topic': {'value': row['topic'], 'evidence': f"Hist. Avg VC: {topic_perf.get(row['topic'], 0):.2f}"},
                    'best_format': {'value': row['format'], 'evidence': f"Hist. Avg VC: {format_perf.get(row['format'], 0):.2f}"},
                    'best_hook': {'value': row['hook_type'], 'evidence': f"Hist. Avg VC: {hook_perf.get(row['hook_type'], 0):.2f}"},
                    'best_time': {'value': row['posting_time'], 'evidence': f"Hist. Avg VC: {time_perf.get(row['posting_time'], 0):.2f}"},
                    'best_cta': {'value': row['cta_type'], 'evidence': f"Hist. Avg VC: {cta_perf.get(row['cta_type'], 0):.2f}"},
                    'platform': row['platform'],
                    'content_type': row['content_type'],
                    'video_length': row['video_length'],
                    'caption_style': row['caption_style'],
                    'hashtag_count': row['hashtag_count'],
                    'audience_segment': row['audience_segment']
                })
        else:
            raise ValueError("Model does not predict HIGH class")
            
    except Exception:
        # Fallback to additive expected value calculation
        overall_mean = df[target_metric].mean()
        candidates_df['additive_score'] = candidates_df.apply(
            lambda r: overall_mean + 
                      (topic_perf.get(r['topic'], overall_mean) - overall_mean) +
                      (format_perf.get(r['format'], overall_mean) - overall_mean) +
                      (hook_perf.get(r['hook_type'], overall_mean) - overall_mean), axis=1
        )
        ranked = candidates_df.sort_values(by='additive_score', ascending=False).head(5)
        
        for idx, row in ranked.iterrows():
            top_strategies.append({
                'expected_metric': {'value': row['additive_score'], 'evidence': 'Additive historical performance (ML fallback)'},
                'best_topic': {'value': row['topic'], 'evidence': f"Hist. Avg VC: {topic_perf.get(row['topic'], 0):.2f}"},
                'best_format': {'value': row['format'], 'evidence': f"Hist. Avg VC: {format_perf.get(row['format'], 0):.2f}"},
                'best_hook': {'value': row['hook_type'], 'evidence': f"Hist. Avg VC: {hook_perf.get(row['hook_type'], 0):.2f}"},
                'best_time': {'value': row['posting_time'], 'evidence': f"Hist. Avg VC: {time_perf.get(row['posting_time'], 0):.2f}"},
                'best_cta': {'value': row['cta_type'], 'evidence': f"Hist. Avg VC: {cta_perf.get(row['cta_type'], 0):.2f}"},
                'platform': row['platform'],
                'content_type': row['content_type'],
                'video_length': row['video_length'],
                'caption_style': row['caption_style'],
                'hashtag_count': row['hashtag_count'],
                'audience_segment': row['audience_segment']
            })
    
    return {'top_strategies': top_strategies}
