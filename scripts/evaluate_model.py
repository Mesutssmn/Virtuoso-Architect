"""
Model Evaluation Script
Evaluates trained model on test set and generates detailed scores.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score
)
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ml_engine.train import load_model, DIFFICULTY_LABELS


def evaluate_model():
    """Evaluate model on test set."""
    
    print("="*70)
    print("MODEL EVALUATION - TEST SET SCORES")
    print("="*70)
    
    # Load model
    model_path = project_root / "models" / "difficulty_classifier.pkl"
    
    if not model_path.exists():
        print("\n❌ Model not found!")
        return
    
    print(f"\n✓ Loading model: {model_path}")
    model = load_model(str(model_path))
    
    # Load data
    features_csv = project_root / "data" / "processed" / "features_all.csv"
    
    if not features_csv.exists():
        print("\n❌ Features file not found!")
        print(f"   Expected: {features_csv}")
        return
    
    print(f"✓ Loading data: {features_csv}")
    df = pd.read_csv(features_csv)
    
    # Features
    feature_cols = [
        'max_stretch', 'max_chord_size', 'note_density',
        'left_hand_activity', 'avg_tempo', 'dynamic_range',
        'poly_voice_count', 'octave_jump_frequency',
        'thirds_frequency', 'polyrhythm_score'
    ]
    
    X = df[feature_cols].values
    
    # Load real labels
    import argparse
    try:
        parser = argparse.ArgumentParser(description='Evaluate model')
        parser.add_argument('--labels', type=str, default='auto_4_labels.csv',
                          help='Label file to use for ground truth (default: auto_4_labels.csv)')
        args = parser.parse_args()
        label_filename = args.labels
    except:
        # Fallback if called from another script without args
        label_filename = 'auto_4_labels.csv'

    labels_csv = project_root / "data" / "processed" / "labels" / label_filename
    
    if not labels_csv.exists():
        print(f"\n❌ Labels file not found: {labels_csv}")
        print(f"   Available files in data/processed/labels/:")
        for f in (project_root / "data" / "processed" / "labels").glob("*.csv"):
            print(f"   - {f.name}")
        return
    
    df_labels = pd.read_csv(labels_csv)
    # Merge with features
    df_merged = df.merge(df_labels, on='midi_filename', how='inner')
    X = df_merged[feature_cols].values
    y_true = df_merged['difficulty_label'].values
    print(f"\n✓ Loaded {len(y_true)} real labels")
    
    # Train-test split (same as training)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_true, test_size=0.2, random_state=42
    )
    
    print(f"\n✓ Test set size: {len(X_test)} samples")
    print(f"✓ Training set size: {len(X_train)} samples")
    
    # Predictions
    print("\n" + "="*70)
    print("MAKING PREDICTIONS...")
    print("="*70)
    
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Basic metrics
    print("\n" + "="*70)
    print("BASIC METRICS")
    print("="*70)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average='weighted'
    )
    
    print(f"\n✓ Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"✓ Precision: {precision:.4f}")
    print(f"✓ Recall: {recall:.4f}")
    print(f"✓ F1-Score: {f1:.4f}")
    
    # Per-class metrics
    print("\n" + "="*70)
    print("DETAILED PER-CLASS METRICS")
    print("="*70)
    
    # Get actual class names for the classes present in data
    unique_classes = np.unique(np.concatenate([y_test, y_pred]))
    class_names = [DIFFICULTY_LABELS.get(i, f"Class-{i}") for i in unique_classes]
    
    print("\nClassification Report:\n")
    print(classification_report(
        y_test, y_pred, 
        target_names=class_names,
        digits=4
    ))
    
    # Confusion Matrix
    print("\n" + "="*70)
    print("CONFUSION MATRIX")
    print("="*70)
    
    cm = confusion_matrix(y_test, y_pred)
    print("\n", cm)
    
    # Confusion Matrix visualization
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names
    )
    plt.title('Confusion Matrix - Test Set', fontsize=14, fontweight='bold')
    plt.ylabel('True Class', fontsize=12)
    plt.xlabel('Predicted Class', fontsize=12)
    plt.tight_layout()
    
    cm_path = project_root / "models" / "confusion_matrix_test.png"
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Confusion matrix saved: {cm_path}")
    plt.close()
    
    # Per-class accuracy
    print("\n" + "="*70)
    print("PER-CLASS ACCURACY")
    print("="*70)
    
    class_accuracies = cm.diagonal() / cm.sum(axis=1)
    
    print("\nCorrect prediction rate for each class:\n")
    for i, (label, acc) in enumerate(zip(class_names, class_accuracies)):
        print(f"  {i}. {label:25s} → {acc:.4f} ({acc*100:.2f}%)")
    
    # Prediction confidence scores
    print("\n" + "="*70)
    print("PREDICTION CONFIDENCE SCORES")
    print("="*70)
    
    confidence_scores = np.max(y_pred_proba, axis=1)
    
    print(f"\nMean confidence score: {np.mean(confidence_scores):.4f}")
    print(f"Min confidence score: {np.min(confidence_scores):.4f}")
    print(f"Max confidence score: {np.max(confidence_scores):.4f}")
    print(f"Median confidence score: {np.median(confidence_scores):.4f}")
    
    # Confidence score distribution
    plt.figure(figsize=(10, 6))
    plt.hist(confidence_scores, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Confidence Score', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Prediction Confidence Score Distribution', fontsize=14, fontweight='bold')
    plt.axvline(np.mean(confidence_scores), color='red', linestyle='--', 
                label=f'Mean: {np.mean(confidence_scores):.3f}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    conf_path = project_root / "models" / "confidence_distribution.png"
    plt.savefig(conf_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Confidence score distribution saved: {conf_path}")
    plt.close()
    
    # Error analysis
    print("\n" + "="*70)
    print("ERROR ANALYSIS")
    print("="*70)
    
    errors = y_test != y_pred
    error_rate = np.mean(errors)
    
    print(f"\nTotal errors: {np.sum(errors)} / {len(y_test)}")
    print(f"Error rate: {error_rate:.4f} ({error_rate*100:.2f}%)")
    
    # Most confused class pairs
    print("\nMost confused class pairs:\n")
    
    confusion_pairs = []
    for i in range(len(unique_classes)):
        for j in range(len(unique_classes)):
            if i != j and cm[i, j] > 0:
                confusion_pairs.append((
                    class_names[i],
                    class_names[j],
                    cm[i, j]
                ))
    
    confusion_pairs.sort(key=lambda x: x[2], reverse=True)
    
    for true_label, pred_label, count in confusion_pairs[:5]:
        print(f"  {true_label:25s} → {pred_label:25s}: {count} times")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    print(f"\n📊 Model Performance:")
    print(f"   • Accuracy: {accuracy*100:.2f}%")
    print(f"   • F1-Score: {f1:.4f}")
    print(f"   • Mean Confidence: {np.mean(confidence_scores):.4f}")
    
    print(f"\n📁 Generated Files:")
    print(f"   • confusion_matrix_test.png")
    print(f"   • confidence_distribution.png")
    
    print(f"\n⚠️  NOTE: Model was trained with random labels,")
    print(f"   so accuracy is low. With real labels, expect 60-80%.")
    
    print("\n✅ Evaluation completed!\n")
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm,
        'confidence_mean': np.mean(confidence_scores)
    }


if __name__ == "__main__":
    results = evaluate_model()
