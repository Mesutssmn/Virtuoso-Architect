"""
Quick Start Script
Automatically runs the entire pipeline:
1. Feature extraction
2. Model training
3. Test analysis
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ml_engine.feature_extract import extract_features_batch
from ml_engine.train import train_model, save_model


def main():
    print("="*70)
    print("VIRTUOSO ARCHITECT - QUICK START")
    print("="*70)
    
    # Step 1: Find MIDI files
    print("\n[1/4] Searching for MIDI files...")
    midi_dir = project_root / "data" / "raw"
    midi_files = list(midi_dir.rglob("*.mid"))
    
    print(f"  ✓ Found {len(midi_files)} MIDI files")
    
    # Ask user: how many files to process?
    print(f"\nHow many files to process?")
    print(f"  1. First 100 files (quick test)")
    print(f"  2. First 1000 files (medium)")
    print(f"  3. All files ({len(midi_files)} files)")
    
    choice = input("\nYour choice (1/2/3) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        midi_files = midi_files[:100]
    elif choice == "2":
        midi_files = midi_files[:1000]
    # choice == "3" keeps all files
    
    print(f"\n  → Processing {len(midi_files)} files")
    
    # Step 2: Feature extraction
    print("\n[2/4] Extracting features...")
    print("  ⚡ Parallel processing active (all CPU cores will be used)")
    
    features_csv = project_root / "data" / "processed" / "features.csv"
    
    df_features = extract_features_batch(
        [str(f) for f in midi_files],
        output_csv=str(features_csv)
    )
    
    print(f"\n  ✓ Extracted features from {len(df_features)} files")
    print(f"  ✓ Saved to: {features_csv}")
    
    # Step 3: Create labels and train model
    print("\n[3/4] Training model...")
    print("  ⚠ Using random labels for demo")
    print("  ⚠ Manual labeling required for real use")
    
    # Prepare features
    feature_cols = [
        'max_stretch', 'max_chord_size', 'note_density',
        'left_hand_activity', 'avg_tempo', 'dynamic_range',
        'poly_voice_count', 'octave_jump_frequency',
        'thirds_frequency', 'polyrhythm_score'
    ]
    X = df_features[feature_cols].values
    
    # Random labels (0-4 range: 5 categories)
    y = np.random.randint(0, 5, len(X))
    
    # Train model
    model_path = project_root / "models" / "difficulty_classifier.pkl"
    model = train_model(X, y, model_save_path=str(model_path))
    
    print(f"\n  ✓ Model trained and saved: {model_path}")
    
    # Step 4: Test analysis
    print("\n[4/4] Running test analysis...")
    
    # Test first MIDI file
    test_file = midi_files[0]
    print(f"\n  Test file: {test_file.name}")
    
    # Import and run main.py
    from main import analyze_midi_file, print_results
    
    results = analyze_midi_file(
        str(test_file),
        str(model_path)
    )
    
    print_results(results)
    
    # Summary
    print("\n" + "="*70)
    print("✓ ALL STEPS COMPLETED!")
    print("="*70)
    print(f"\nModel location: {model_path}")
    print(f"Features: {features_csv}")
    print(f"\nTo analyze any MIDI file:")
    print(f'  .venv\\Scripts\\python.exe src/main.py --midi_file "file_path.mid"')
    print("\n")


if __name__ == "__main__":
    main()
