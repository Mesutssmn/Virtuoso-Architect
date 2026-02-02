"""
XGBoost Classifier for Piano Technical Difficulty Classification
Classifies pieces into 5 technical difficulty categories.
"""

import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import os
from pathlib import Path


# The 5 Technical Difficulty Categories
DIFFICULTY_LABELS = {
    0: "Far Reach",              # Wide hand spans (e.g., Rachmaninoff)
    1: "Double Thirds",          # Technical runs in thirds (e.g., Chopin)
    2: "Multiple Voices",        # Polyphony (e.g., Bach)
    3: "Advanced Chords",        # Dense textures (e.g., Brahms)
    4: "Advanced Counterpoint"   # Precision/Independence (e.g., Mozart)
}

LABEL_TO_ID = {v: k for k, v in DIFFICULTY_LABELS.items()}


def prepare_training_data(features_csv, labels_csv=None):
    """
    Prepare training data from features and labels.
    
    Args:
        features_csv (str): Path to features CSV file
        labels_csv (str, optional): Path to labels CSV file
        
    Returns:
        tuple: (X, y) features and labels, or just X if no labels
    """
    # Load features
    df_features = pd.read_csv(features_csv)
    
    # Select all 10 feature columns
    feature_cols = [
        'max_stretch', 'max_chord_size', 'note_density',
        'left_hand_activity', 'avg_tempo', 'dynamic_range',
        'poly_voice_count', 'octave_jump_frequency', 
        'thirds_frequency', 'polyrhythm_score'
    ]
    X = df_features[feature_cols].values
    
    if labels_csv:
        # Load labels
        df_labels = pd.read_csv(labels_csv)
        
        # Merge on filename
        df_merged = df_features.merge(df_labels, on='midi_filename', how='inner')
        
        # Get labels
        y = df_merged['difficulty_label'].values
        
        return X, y
    
    return X, None


def train_model(X, y, model_save_path=None, test_size=0.2, random_state=42):
    """
    Train XGBoost classifier on the data.
    
    Args:
        X (np.ndarray): Feature matrix
        y (np.ndarray): Labels
        model_save_path (str, optional): Path to save trained model
        test_size (float): Proportion of test set
        random_state (int): Random seed
        
    Returns:
        xgb.XGBClassifier: Trained model
    """
    print("Training XGBoost classifier...")
    print(f"Dataset size: {len(X)} samples")
    print(f"Number of features: {X.shape[1]} (10 comprehensive features)")
    print(f"Number of classes: {len(np.unique(y))}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Create and train model
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        objective='multi:softmax',
        num_class=len(DIFFICULTY_LABELS),
        random_state=random_state,
        eval_metric='mlogloss'
    )
    
    # Train
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=True
    )
    
    # Evaluate
    y_pred = model.predict(X_test)
    
    print("\n" + "="*50)
    print("Model Evaluation")
    print("="*50)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=list(DIFFICULTY_LABELS.values())))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"\nCross-validation scores: {cv_scores}")
    print(f"Mean CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    # Save model
    if model_save_path:
        save_model(model, model_save_path)
    
    return model


def save_model(model, save_path):
    """
    Save trained model to disk.
    
    Args:
        model: Trained XGBoost model
        save_path (str): Path to save model
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"✓ Model saved to: {save_path}")


def load_model(model_path):
    """
    Load trained model from disk.
    
    Args:
        model_path (str): Path to saved model
        
    Returns:
        Trained XGBoost model
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"✓ Model loaded from: {model_path}")
    return model


def predict_difficulty(model, features):
    """
    Predict difficulty category for given features.
    
    Args:
        model: Trained XGBoost model
        features (dict or np.ndarray): Feature dictionary or array
        
    Returns:
        dict: Prediction results with label and probabilities
    """
    # Convert features dict to array if needed
    if isinstance(features, dict):
        feature_array = np.array([
            features.get('max_stretch', 0),
            features.get('max_chord_size', 0),
            features.get('note_density', 0),
            features.get('left_hand_activity', 0),
            features.get('avg_tempo', 120),
            features.get('dynamic_range', 0),
            features.get('poly_voice_count', 1),
            features.get('octave_jump_frequency', 0),
            features.get('thirds_frequency', 0),
            features.get('polyrhythm_score', 0)
        ]).reshape(1, -1)
    else:
        feature_array = features.reshape(1, -1)
    
    # Predict
    pred_id = model.predict(feature_array)[0]
    pred_proba = model.predict_proba(feature_array)[0]
    
    # Get label
    pred_label = DIFFICULTY_LABELS[pred_id]
    
    # Create probability dict
    proba_dict = {DIFFICULTY_LABELS[i]: float(prob) for i, prob in enumerate(pred_proba)}
    
    return {
        'predicted_category': pred_label,
        'predicted_id': int(pred_id),
        'confidence': float(pred_proba[pred_id]),
        'probabilities': proba_dict
    }


if __name__ == "__main__":
    # Example usage
    print("XGBoost Difficulty Classifier")
    print("="*50)
    print("\nDifficulty Categories:")
    for id, label in DIFFICULTY_LABELS.items():
        print(f"  {id}: {label}")
