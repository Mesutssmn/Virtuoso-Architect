"""
Quick Start - ALL FILES
Processes all MIDI files (10,841+ files)
Optimized version - Estimated time: 6-10 hours
"""

import sys
from pathlib import Path
import pandas as pd
import time

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ml_engine.feature_extract import extract_features_batch
from ml_engine.train import train_model, save_model
import numpy as np


def main():
    print("="*70)
    print("VIRTUOSO ARCHITECT - PROCESSING ALL FILES")
    print("="*70)
    
    # Step 1: Find MIDI files
    print("\n[1/4] Searching for MIDI files...")
    midi_dir = project_root / "data" / "raw"
    midi_files = list(midi_dir.rglob("*.mid"))
    
    print(f"  ✓ Found {len(midi_files)} MIDI files")
    
    # Time estimation (with parallel processing)
    import multiprocessing as mp
    n_cores = max(1, mp.cpu_count() - 1)
    estimated_time_hours = (len(midi_files) * 2) / (3600 * n_cores)  # ~2 sec/file, parallel
    
    print(f"\n  💻 CPU cores to use: {n_cores} (out of {mp.cpu_count()})")
    print(f"  ⏱️  Estimated time: {estimated_time_hours:.1f} hours (with parallel processing)")
    print(f"  ⚠️  This is a long process! Don't turn off your computer.")
    print(f"  ℹ️  1-2 cores will be kept free to prevent system freeze")
    
    response = input("\n  Do you want to continue? (y/n) [y]: ").strip().lower() or "y"
    
    if response != "y":
        print("\n  Process cancelled.")
        return
    
    # Step 2: Feature extraction
    print("\n[2/4] Extracting features...")
    print("  (This process may take several hours...)")
    
    features_csv = project_root / "data" / "processed" / "features_all.csv"
    
    start_time = time.time()
    
    df_features = extract_features_batch(
        [str(f) for f in midi_files],
        output_csv=str(features_csv)
    )
    
    elapsed_time = time.time() - start_time
    elapsed_hours = elapsed_time / 3600
    
    print(f"\n  ✓ Extracted features from {len(df_features)} files")
    print(f"  ✓ Elapsed time: {elapsed_hours:.2f} hours")
    print(f"  ✓ Saved to: {features_csv}")
    
    # Step 3: Create labels and train model
    print("\n[3/4] Training model...")
    print("  ⚠ Using random labels for demo")
    
    # Prepare features
    feature_cols = [
        'max_stretch', 'max_chord_size', 'note_density',
        'left_hand_activity', 'avg_tempo', 'dynamic_range',
        'poly_voice_count', 'octave_jump_frequency',
        'thirds_frequency', 'polyrhythm_score'
    ]
    X = df_features[feature_cols].values
    
    # Random labels (0-4 range: 5 categories)
    np.random.seed(42)  # For reproducibility
    y = np.random.randint(0, 5, len(X))
    
    # Train model
    model_path = project_root / "models" / "difficulty_classifier_full.pkl"
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
    print(f"\nTotal files processed: {len(df_features)}")
    print(f"Total time: {elapsed_hours:.2f} hours")
    print(f"Model location: {model_path}")
    print(f"Features: {features_csv}")
    print(f"\nTo analyze any MIDI file:")
    print(f'  .venv\\Scripts\\python.exe src/main.py --midi_file "file_path.mid" --model "{model_path}"')
    print("\n")


if __name__ == "__main__":
    main()
