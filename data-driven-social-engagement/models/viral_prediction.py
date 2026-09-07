import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'saved_models')
os.makedirs(MODELS_DIR, exist_ok=True)

class ViralityPredictor:
    def __init__(self):
        self.features = [
            'platform', 'topic', 'content_type', 'format', 'hook_type', 'posting_time', 
            'cta_type', 'caption_style', 'audience_segment', 
            'video_length', 'hashtag_count'
        ]
        
        # Identify categorical features to one-hot encode
        self.categorical_features = [
            'platform', 'topic', 'content_type', 'format', 'hook_type', 'posting_time', 
            'cta_type', 'caption_style', 'audience_segment'
        ]
        
        # Build the Preprocessing ColumnTransformer
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), self.categorical_features)
            ],
            remainder='passthrough' # Leave numerical features as they are
        )
        
        # Build the final Pipeline
        self.pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
    def generate_target(self, df):
        """
        Creates Target Variable based on actual engagement outcomes (Viral Coefficient).
        The model predicts viral potential from pre-publication characteristics, while the 
        target is derived from observed post-publication performance.
        Classifies into LOW, MEDIUM, HIGH based on quantiles.
        """
        df_ml = df.copy()
        if 'viral_coefficient' not in df_ml.columns:
            return None, None
            
        quantiles = df_ml['viral_coefficient'].quantile([0.33, 0.66])
        
        def classify_viral(score):
            if score <= quantiles[0.33]:
                return 'LOW'
            elif score <= quantiles[0.66]:
                return 'MEDIUM'
            else:
                return 'HIGH'
                
        df_ml['viral_potential'] = df_ml['viral_coefficient'].apply(classify_viral)
        
        X = df_ml[self.features].copy()
        y = df_ml['viral_potential']
        return X, y

    def train_and_evaluate(self, df):
        X, y = self.generate_target(df)
        if X is None:
            return None
            
        # Split first to prevent data leakage during categorical encoding
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Fit the entire pipeline ONLY on training data
        self.pipeline.fit(X_train, y_train)
        
        # Evaluate on test data
        y_pred = self.pipeline.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred, labels=['LOW', 'MEDIUM', 'HIGH']).tolist(),
            'classes': ['LOW', 'MEDIUM', 'HIGH'],
            'train_size': len(X_train),
            'test_size': len(X_test)
        }
        
        # Extract feature importances
        # We need to get the feature names after one-hot encoding
        try:
            cat_features_encoded = self.pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(self.categorical_features)
            num_features = [f for f in self.features if f not in self.categorical_features]
            all_feature_names = list(cat_features_encoded) + num_features
            
            importance = self.pipeline.named_steps['classifier'].feature_importances_
            feature_importance = pd.DataFrame({
                'Feature': all_feature_names,
                'Importance': importance
            }).sort_values(by='Importance', ascending=False).head(20) # Top 20 for brevity
            
            metrics['feature_importance'] = feature_importance.to_dict('records')
        except Exception:
            metrics['feature_importance'] = []
        
        # Save pipeline
        joblib.dump(self.pipeline, os.path.join(MODELS_DIR, 'viral_rf_model.pkl'))
        
        return metrics
