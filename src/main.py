"""
Main Coordinator for Virtuoso Architect
Orchestrates MIDI feature extraction and ML classification.
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from ml_engine.feature_extract import extract_features_from_midi
from ml_engine.train import load_model, predict_difficulty, DIFFICULTY_LABELS


def analyze_midi_file(midi_path, model_path, piece_info=None):
    """
    Complete analysis pipeline for a MIDI file.
    
    Args:
        midi_path (str): Path to MIDI file
        model_path (str): Path to trained model
        piece_info (dict, optional): Piece metadata (composer, title)
        
    Returns:
        dict: Complete analysis results
    """
    print(f"\n{'='*60}")
    print(f"Analyzing: {Path(midi_path).name}")
    print(f"{'='*60}\n")
    
    # Step 1: Extract features
    print("Step 1/2: Extracting features...")
    features = extract_features_from_midi(midi_path)
    
    if not features:
        return {'error': 'Failed to extract features from MIDI file'}
    
    print(f"  ✓ Max stretch: {features['max_stretch']} semitones")
    print(f"  ✓ Max chord size: {features['max_chord_size']} notes")
    print(f"  ✓ Note density: {features['note_density']:.2f} notes/second")
    
    # Step 2: Classify difficulty
    print("\nStep 2/2: Classifying technical difficulty...")
    
    try:
        model = load_model(model_path)
        prediction = predict_difficulty(model, features)
        
        print(f"  ✓ Category: {prediction['predicted_category']}")
        print(f"  ✓ Confidence: {prediction['confidence']:.2%}")
        
    except FileNotFoundError:
        print("  ⚠ Model not found. Using fallback classification...")
        # Simple rule-based fallback
        if features['max_stretch'] > 12:
            category = "Far Reach"
        elif features['max_chord_size'] > 5:
            category = "Advanced Chords"
        elif features['note_density'] > 10:
            category = "Double Thirds"
        else:
            category = "Multiple Voices"
        
        prediction = {
            'predicted_category': category,
            'predicted_id': list(DIFFICULTY_LABELS.values()).index(category),
            'confidence': 0.5,
            'probabilities': {},
            'note': 'Using fallback classification (model not trained)'
        }
    
    # Combine results
    results = {
        'file': str(midi_path),
        'piece_info': piece_info or {},
        'features': features,
        'classification': prediction
    }
    
    return results


def print_results(results):
    """
    Pretty print analysis results.
    
    Args:
        results (dict): Analysis results
    """
    print(f"\n{'='*60}")
    print("ANALYSIS RESULTS")
    print(f"{'='*60}\n")
    
    # Classification
    print("🎹 TECHNICAL CLASSIFICATION")
    print(f"   Category: {results['classification']['predicted_category']}")
    print(f"   Category ID: {results['classification']['predicted_id']}")
    print(f"   Confidence: {results['classification']['confidence']:.2%}")
    
    # Show all probabilities if available
    if results['classification'].get('probabilities'):
        print(f"\n   All Category Probabilities:")
        for category, prob in results['classification']['probabilities'].items():
            print(f"   • {category}: {prob:.2%}")
    
    # Features
    print(f"\n📊 EXTRACTED FEATURES (10 total)")
    print(f"   Max Stretch: {results['features']['max_stretch']:.2f} semitones")
    print(f"   Max Chord Size: {results['features']['max_chord_size']} notes")
    print(f"   Note Density: {results['features']['note_density']:.2f} notes/sec")
    print(f"   Left Hand Activity: {results['features']['left_hand_activity']:.2%}")
    print(f"   Average Tempo: {results['features']['avg_tempo']:.0f} BPM")
    print(f"   Dynamic Range: {results['features']['dynamic_range']:.2f}")
    print(f"   Polyphony (Voice Count): {results['features']['poly_voice_count']:.2f}")
    print(f"   Octave Jump Frequency: {results['features']['octave_jump_frequency']:.2%}")
    print(f"   Thirds Frequency: {results['features']['thirds_frequency']:.2%}")
    print(f"   Polyrhythm Score: {results['features']['polyrhythm_score']:.2f}")
    
    # Piece info if available
    if results.get('piece_info'):
        print(f"\n🎼 PIECE INFORMATION")
        if results['piece_info'].get('composer'):
            print(f"   Composer: {results['piece_info']['composer']}")
        if results['piece_info'].get('title'):
            print(f"   Title: {results['piece_info']['title']}")
    
    print(f"\n{'='*60}\n")


def main():
    """
    Main CLI interface.
    """
    parser = argparse.ArgumentParser(
        description="Virtuoso Architect - Piano MIDI Technical Analysis"
    )
    
    parser.add_argument(
        '--midi_file',
        type=str,
        required=True,
        help='Path to MIDI file to analyze'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='models/difficulty_classifier.pkl',
        help='Path to trained model (default: models/difficulty_classifier.pkl)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Path to save JSON results (optional)'
    )
    
    parser.add_argument(
        '--composer',
        type=str,
        help='Composer name (optional)'
    )
    
    parser.add_argument(
        '--title',
        type=str,
        help='Piece title (optional)'
    )
    
    args = parser.parse_args()
    
    # Prepare piece info
    piece_info = {}
    if args.composer:
        piece_info['composer'] = args.composer
    if args.title:
        piece_info['title'] = args.title
    
    # Run analysis
    results = analyze_midi_file(
        args.midi_file,
        args.model,
        piece_info=piece_info if piece_info else None
    )
    
    # Print results
    print_results(results)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✓ Results saved to: {args.output}")


if __name__ == "__main__":
    main()
