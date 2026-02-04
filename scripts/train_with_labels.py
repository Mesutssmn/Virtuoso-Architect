"""
Train Model with Real Labels
Uses manually labeled data instead of random labels.
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ml_engine.train import prepare_training_data, train_model

def main():
    print("="*70)
    print("TRAINING WITH REAL LABELS")
    print("="*70)
    
    # Paths
    features_csv = project_root / "data" / "processed" / "features_all.csv"
    labels_csv = project_root / "data" / "processed" / "labels.csv"
    model_path = project_root / "models" / "difficulty_classifier.pkl"
    
    # Check if labels exist
    if not labels_csv.exists():
        print("\n❌ Labels file not found!")
        print(f"   Expected: {labels_csv}")
        print("\n   Please label some files first:")
        print("   .venv\\Scripts\\python.exe tools/start_labeling.py")
        return
    
    # Load labels to check count
    labels_df = pd.read_csv(labels_csv)
    print(f"\n✓ Found {len(labels_df)} labeled files")
    
    if len(labels_df) < 50:
        print(f"\n⚠️  WARNING: Only {len(labels_df)} labeled files!")
        print("   Recommended: At least 50-100 files for meaningful training")
        print("   Current labels may not be enough for good accuracy")
        
        response = input("\n   Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            print("\n   Training cancelled. Label more files first.")
            return
    
    # Prepare data
    print("\n[1/3] Preparing training data...")
    X, y = prepare_training_data(str(features_csv), str(labels_csv))
    
    if X is None or y is None:
        print("\n❌ Failed to prepare training data!")
        return
    
    # Check label distribution
    print("\n📊 Label Distribution:")
    unique, counts = pd.Series(y).value_counts().sort_index().items(), pd.Series(y).value_counts().sort_index().values
    
    from ml_engine.train import DIFFICULTY_LABELS
    for label_id, count in zip(range(5), counts if len(counts) == 5 else [0]*5):
        label_name = DIFFICULTY_LABELS.get(label_id, f"Unknown-{label_id}")
        actual_count = counts[label_id] if label_id < len(counts) else 0
        print(f"   {label_id}: {label_name:30s} → {actual_count} files")
    
    # Check for imbalanced data
    if len(counts) > 0:
        max_count = max(counts)
        min_count = min(counts)
        if max_count / min_count > 5:
            print(f"\n⚠️  WARNING: Imbalanced dataset detected!")
            print(f"   Max: {max_count}, Min: {min_count}")
            print(f"   Consider labeling more files for underrepresented classes")
    
    # Train model
    print("\n[2/3] Training model...")
    model = train_model(X, y, model_save_path=str(model_path))
    
    print(f"\n[3/3] Model saved to: {model_path}")
    
    # Summary
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETED!")
    print("="*70)
    print(f"\n📊 Training Summary:")
    print(f"   • Total samples: {len(X)}")
    print(f"   • Features: 10")
    print(f"   • Classes: 5")
    print(f"   • Model: XGBoost Classifier")
    
    print(f"\n📁 Files:")
    print(f"   • Model: {model_path}")
    print(f"   • Labels: {labels_csv}")
    
    print(f"\n🔍 Next Steps:")
    print(f"   1. Evaluate model:")
    print(f"      .venv\\Scripts\\python.exe scripts/evaluate_model.py")
    print(f"\n   2. If accuracy is low, label more files:")
    print(f"      .venv\\Scripts\\python.exe tools/start_labeling.py")
    print(f"\n   3. Analyze model:")
    print(f"      .venv\\Scripts\\python.exe scripts/analyze_model.py")
    print("\n")

if __name__ == "__main__":
    main()
