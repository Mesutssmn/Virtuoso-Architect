"""
Simple Test Script
Tests feature extraction on a sample MIDI file from the dataset.
"""

import sys
from pathlib import Path
import os

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from ml_engine.feature_extract import extract_features_from_midi


def main():
    """
    Test feature extraction on a sample MIDI file.
    """
    print("="*60)
    print("Testing Feature Extraction")
    print("="*60)
    
    # Find a MIDI file in data/raw
    midi_dir = project_root / "data" / "raw"
    
    if not midi_dir.exists():
        print(f"\n❌ MIDI directory not found: {midi_dir}")
        return
    
    # Find first MIDI file
    midi_files = list(midi_dir.rglob("*.mid"))
    
    if not midi_files:
        print(f"\n❌ No MIDI files found in {midi_dir}")
        return
    
    # Test on first file
    test_file = midi_files[0]
    print(f"\nTesting on: {test_file.name}")
    print(f"Full path: {test_file}")
    
    # Extract features
    print("\nExtracting features...")
    features = extract_features_from_midi(str(test_file))
    
    if features:
        print("\n✓ Feature extraction successful!")
        print("\nExtracted Features (10 total):")
        print(f"  • Max Stretch: {features['max_stretch']:.2f} semitones")
        print(f"  • Max Chord Size: {features['max_chord_size']} notes")
        print(f"  • Note Density: {features['note_density']:.2f} notes/second")
        print(f"  • Left Hand Activity: {features['left_hand_activity']:.2%}")
        print(f"  • Average Tempo: {features['avg_tempo']:.0f} BPM")
        print(f"  • Dynamic Range: {features['dynamic_range']:.2f}")
        print(f"  • Polyphony (Voice Count): {features['poly_voice_count']:.2f}")
        print(f"  • Octave Jump Frequency: {features['octave_jump_frequency']:.2%}")
        print(f"  • Thirds Frequency: {features['thirds_frequency']:.2%}")
        print(f"  • Polyrhythm Score: {features['polyrhythm_score']:.2f}")
        
        print("\n" + "="*60)
        print("✓ Test completed successfully!")
        print("="*60)
        
        print("\nYou can now analyze any MIDI file with:")
        print(f"  python src/main.py --midi_file \"{test_file}\"")
        
    else:
        print("\n❌ Feature extraction failed!")


if __name__ == "__main__":
    main()
