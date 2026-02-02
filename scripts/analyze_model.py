"""
Model Analysis Script
Analyzes trained model performance and feature importance.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ml_engine.train import load_model, DIFFICULTY_LABELS


def analyze_model_performance():
    """Analyze model performance and feature importance."""
    
    print("="*70)
    print("MODEL PERFORMANCE ANALYSIS")
    print("="*70)
    
    # Load model
    model_path = project_root / "models" / "difficulty_classifier.pkl"
    
    if not model_path.exists():
        print("\n❌ Model not found!")
        print(f"   Expected location: {model_path}")
        print("\n   First train the model:")
        print("   .venv\\Scripts\\python.exe scripts/quick_start.py")
        return
    
    print(f"\n✓ Loading model: {model_path}")
    model = load_model(str(model_path))
    
    # Feature names
    feature_names = [
        'Max Stretch', 'Max Chord Size', 'Note Density',
        'Left Hand Activity', 'Avg Tempo', 'Dynamic Range',
        'Polyphony', 'Octave Jumps', 'Thirds Freq', 'Polyrhythm'
    ]
    
    # Feature importances
    print("\n" + "="*70)
    print("FEATURE IMPORTANCES")
    print("="*70)
    
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        
        # Sort
        indices = np.argsort(importances)[::-1]
        
        print("\nImportance ranking (most to least important):\n")
        for i, idx in enumerate(indices, 1):
            print(f"  {i}. {feature_names[idx]:25s} → {importances[idx]:.4f}")
        
        # Create graph
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(importances)), importances[indices], color='steelblue')
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.xlabel('Features', fontsize=12)
        plt.ylabel('Importance Score', fontsize=12)
        plt.title('Feature Importances - XGBoost Model', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        # Save
        output_path = project_root / "models" / "feature_importance.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Graph saved: {output_path}")
        plt.close()
    
    # Dataset statistics
    print("\n" + "="*70)
    print("DATASET STATISTICS")
    print("="*70)
    
    features_csv = project_root / "data" / "processed" / "features.csv"
    
    if features_csv.exists():
        df = pd.read_csv(features_csv)
        
        print(f"\n✓ Total files: {len(df)}")
        print(f"✓ Total features: 10")
        
        # Feature statistics
        print("\nFeature Statistics:\n")
        
        feature_cols = [
            'max_stretch', 'max_chord_size', 'note_density',
            'left_hand_activity', 'avg_tempo', 'dynamic_range',
            'poly_voice_count', 'octave_jump_frequency',
            'thirds_frequency', 'polyrhythm_score'
        ]
        
        stats = df[feature_cols].describe()
        print(stats.to_string())
        
        # Correlation matrix
        print("\n" + "="*70)
        print("FEATURE CORRELATION")
        print("="*70)
        
        corr = df[feature_cols].corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', 
                    xticklabels=feature_names, yticklabels=feature_names,
                    center=0, vmin=-1, vmax=1)
        plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        corr_path = project_root / "models" / "feature_correlation.png"
        plt.savefig(corr_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Correlation matrix saved: {corr_path}")
        plt.close()
        
        # Distribution graphs
        print("\n" + "="*70)
        print("FEATURE DISTRIBUTIONS")
        print("="*70)
        
        fig, axes = plt.subplots(5, 2, figsize=(15, 18))
        axes = axes.flatten()
        
        for i, (col, name) in enumerate(zip(feature_cols, feature_names)):
            axes[i].hist(df[col].dropna(), bins=50, color='steelblue', edgecolor='black', alpha=0.7)
            axes[i].set_title(name, fontweight='bold')
            axes[i].set_xlabel('Value')
            axes[i].set_ylabel('Frequency')
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        dist_path = project_root / "models" / "feature_distributions.png"
        plt.savefig(dist_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Distribution graphs saved: {dist_path}")
        plt.close()
    
    # Model parameters
    print("\n" + "="*70)
    print("MODEL PARAMETERS")
    print("="*70)
    
    print(f"\nModel type: XGBoost Classifier")
    print(f"Number of classes: {len(DIFFICULTY_LABELS)}")
    print(f"\nClasses:")
    for id, label in DIFFICULTY_LABELS.items():
        print(f"  {id}: {label}")
    
    if hasattr(model, 'get_params'):
        params = model.get_params()
        print(f"\nImportant parameters:")
        print(f"  • n_estimators: {params.get('n_estimators', 'N/A')}")
        print(f"  • max_depth: {params.get('max_depth', 'N/A')}")
        print(f"  • learning_rate: {params.get('learning_rate', 'N/A')}")
        print(f"  • objective: {params.get('objective', 'N/A')}")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    print("\n✅ Model analysis completed!")
    print(f"\n📊 Generated graphs:")
    print(f"   1. feature_importance.png - Feature importances")
    print(f"   2. feature_correlation.png - Correlation matrix")
    print(f"   3. feature_distributions.png - Feature distributions")
    print(f"\n📁 Location: {project_root / 'models'}")
    print("\n")


if __name__ == "__main__":
    analyze_model_performance()
