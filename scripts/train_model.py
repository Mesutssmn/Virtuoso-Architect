"""
Model Training Script
Trains XGBoost classifier on extracted features.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ml_engine.train import train_model, DIFFICULTY_LABELS
from ml_engine.feature_extract import extract_features_batch


def create_sample_labels(num_samples):
    """
    Create sample labels for demonstration.
    In production, these would come from manual annotation.
    
    Args:
        num_samples (int): Number of samples
        
    Returns:
        np.ndarray: Random labels
    """
    print("\n⚠ WARNING: Using randomly generated labels for demonstration")
    print("   In production, you should have manually annotated labels")
    return np.random.randint(0, len(DIFFICULTY_LABELS), num_samples)


def main():
    """
    Main training function.
    """
    print("="*60)
    print("XGBoost Model Training")
    print("="*60)
    
    # Define paths
    features_csv = project_root / "data" / "processed" / "features.csv"
    model_save_path = project_root / "models" / "difficulty_classifier.pkl"
    
    # Check if features exist
    if not features_csv.exists():
        print(f"\n❌ Features file not found: {features_csv}")
        print("\nYou need to extract features first. Options:")
        print("  1. Run feature extraction on your MIDI files")
        print("  2. Use the feature_extract.py module")
        
        # Offer to extract features from sample files
        midi_dir = project_root / "data" / "raw"
        if midi_dir.exists():
            midi_files = list(midi_dir.glob("*.mid"))[:100]  # Limit to 100 for demo
            
            if midi_files:
                print(f"\nFound {len(midi_files)} MIDI files in {midi_dir}")
                response = input("Extract features from these files? (y/n): ")
                
                if response.lower() == 'y':
                    print("\nExtracting features...")
                    df_features = extract_features_batch(
                        [str(f) for f in midi_files],
                        output_csv=str(features_csv)
                    )
                else:
                    return
            else:
                print(f"\nNo MIDI files found in {midi_dir}")
                return
        else:
            return
    
    # Load features
    print(f"\nLoading features from: {features_csv}")
    df = pd.read_csv(features_csv)
    
    # Prepare data
    feature_cols = [
        'max_stretch', 'max_chord_size', 'note_density',
        'left_hand_activity', 'avg_tempo', 'dynamic_range',
        'poly_voice_count', 'octave_jump_frequency',
        'thirds_frequency', 'polyrhythm_score'
    ]
    X = df[feature_cols].values
    
    # Create or load labels
    # NOTE: In production, you should have a labels CSV with manual annotations
    print("\n⚠ Creating sample labels (replace with real annotations in production)")
    y = create_sample_labels(len(X))
    
    print(f"\nDataset info:")
    print(f"  Samples: {len(X)}")
    print(f"  Features: {X.shape[1]}")
    print(f"  Classes: {len(np.unique(y))}")
    
    # Train model
    print("\nStarting training...")
    model = train_model(X, y, model_save_path=str(model_save_path))
    
    print("\n" + "="*60)
    print("✓ Training completed!")
    print("="*60)
    print(f"\nModel saved to: {model_save_path}")
    print("\nYou can now use the model with:")
    print(f"  python src/main.py --midi_file <path_to_midi>")


if __name__ == "__main__":
    main()
