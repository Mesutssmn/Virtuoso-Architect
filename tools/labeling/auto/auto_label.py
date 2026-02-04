"""
Automatic MIDI Difficulty Labeling
Supports both 4-label and 5-label configurations
"""

import sys
from pathlib import Path
import pandas as pd
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.labeling.config import get_labels, get_thresholds, get_num_classes, print_config_summary


def auto_label_file_4(features: dict) -> int:
    """
    Auto-label with 4 categories
    0: Far Reach, 1: Double Thirds, 2: Advanced Chords, 3: Advanced Counterpoint
    """
    # Extract features
    max_stretch = features.get('max_stretch', 0)
    thirds_freq = features.get('thirds_frequency', 0)
    max_chord = features.get('max_chord_size', 0)
    note_density = features.get('note_density', 0)
    left_hand = features.get('left_hand_activity', 0)
    poly_voices = features.get('poly_voice_count', 0)
    octave_jumps = features.get('octave_jump_frequency', 0)
    polyrhythm = features.get('polyrhythm_score', 0)
    
    # Score each category
    scores = {0: 0, 1: 0, 2: 0, 3: 0}
    
    # Far Reach (0)
    if max_stretch > 25:
        scores[0] += 3
    elif max_stretch > 20:
        scores[0] += 2
    if octave_jumps > 0.15:
        scores[0] += 2
    
    # Double Thirds (1)
    if thirds_freq > 0.30:
        scores[1] += 4
    elif thirds_freq > 0.22:
        scores[1] += 2
    if note_density > 8 and thirds_freq > 0.20:
        scores[1] += 1
    
    # Advanced Chords (2)
    if max_chord > 9:
        scores[2] += 4
    elif max_chord > 7:
        scores[2] += 2
    if note_density > 10:
        scores[2] += 2
    
    # Advanced Counterpoint (3)
    if poly_voices > 3:
        scores[3] += 2
    if left_hand > 0.35:
        scores[3] += 2
    if polyrhythm > 0.25:
        scores[3] += 2
    if octave_jumps > 0.20 and poly_voices > 2:
        scores[3] += 1
    
    # Get winner
    max_score = max(scores.values())
    
    # Fallback if no clear winner
    if max_score < 3:
        if thirds_freq > 0.22:
            return 1
        elif max_chord > 7:
            return 2
        elif poly_voices > 2.5:
            return 3
        else:
            return 0
    
    # Return highest scoring category
    winners = [cat for cat, score in scores.items() if score == max_score]
    if len(winners) > 1:
        # Priority: Double Thirds > Advanced Chords > Counterpoint > Far Reach
        for priority in [1, 2, 3, 0]:
            if priority in winners:
                return priority
    
    return winners[0]


def auto_label_file_5(features: dict) -> int:
    """
    Auto-label with 5 categories
    0: Far Reach, 1: Double Thirds, 2: Multiple Voices, 3: Advanced Chords, 4: Advanced Counterpoint
    """
    # Extract features
    max_stretch = features.get('max_stretch', 0)
    thirds_freq = features.get('thirds_frequency', 0)
    max_chord = features.get('max_chord_size', 0)
    note_density = features.get('note_density', 0)
    left_hand = features.get('left_hand_activity', 0)
    poly_voices = features.get('poly_voice_count', 0)
    octave_jumps = features.get('octave_jump_frequency', 0)
    polyrhythm = features.get('polyrhythm_score', 0)
    
    # Score each category
    scores = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    
    # Far Reach (0)
    if max_stretch > 25:
        scores[0] += 3
    elif max_stretch > 20:
        scores[0] += 2
    if octave_jumps > 0.15:
        scores[0] += 2
    
    # Double Thirds (1)
    if thirds_freq > 0.30:
        scores[1] += 4
    elif thirds_freq > 0.22:
        scores[1] += 2
    if note_density > 8 and thirds_freq > 0.20:
        scores[1] += 1
    
    # Multiple Voices (2) - NEW!
    # Key: Polyphonic but NOT overly dense chords
    if poly_voices > 3.5:
        scores[2] += 3
    elif poly_voices > 3:
        scores[2] += 2
    if left_hand > 0.40 and max_chord < 8:  # Active left hand, moderate chords
        scores[2] += 2
    if poly_voices > 3 and polyrhythm > 0.15:  # Voice independence
        scores[2] += 2
    
    # Advanced Chords (3)
    if max_chord > 9:
        scores[3] += 4
    elif max_chord > 7:
        scores[3] += 2
    if note_density > 10:
        scores[3] += 2
    
    # Advanced Counterpoint (4)
    if poly_voices > 4:
        scores[4] += 2
    if left_hand > 0.45:
        scores[4] += 2
    if polyrhythm > 0.30:
        scores[4] += 3
    if octave_jumps > 0.20 and poly_voices > 3:
        scores[4] += 1
    
    # Get winner
    max_score = max(scores.values())
    
    # Fallback if no clear winner
    if max_score < 3:
        if thirds_freq > 0.22:
            return 1
        elif poly_voices > 3.5 and max_chord < 8:
            return 2  # Multiple Voices
        elif max_chord > 7:
            return 3
        elif poly_voices > 3 or polyrhythm > 0.20:
            return 4
        else:
            return 0
    
    # Return highest scoring category
    winners = [cat for cat, score in scores.items() if score == max_score]
    if len(winners) > 1:
        # Priority: Double Thirds > Multiple Voices > Advanced Chords > Counterpoint > Far Reach
        for priority in [1, 2, 3, 4, 0]:
            if priority in winners:
                return priority
    
    return winners[0]


def auto_label_all(features_csv: Path, output_csv: Path, config: str = "5_labels", overwrite: bool = False):
    """Auto-label all files in features CSV"""
    
    print(f"\n{'='*70}")
    print(f"AUTOMATIC LABELING - {config.upper()}")
    print(f"{'='*70}\n")
    
    # Print configuration
    print_config_summary(config)
    
    # Check if output exists
    if output_csv.exists() and not overwrite:
        print(f"\n❌ Output file already exists: {output_csv}")
        print("   Use --overwrite to replace it")
        return
    
    # Load features
    print(f"\n📂 Loading features from: {features_csv}")
    df_features = pd.read_csv(features_csv)
    print(f"✓ Loaded {len(df_features)} files")
    
    # Select labeling function
    if config == "4_labels":
        label_func = auto_label_file_4
    elif config == "5_labels":
        label_func = auto_label_file_5
    else:
        raise ValueError(f"Unknown config: {config}")
    
    # Label each file
    print(f"\n🏷️  Labeling files...")
    labels = []
    
    for idx, row in df_features.iterrows():
        features = row.to_dict()
        label = label_func(features)
        labels.append({
            'midi_filename': row['midi_filename'],
            'difficulty_label': label,
            'timestamp': datetime.now().isoformat(),
            'confidence': 3,  # Auto-labeled
            'method': f'auto_{config}'
        })
        
        if (idx + 1) % 1000 == 0:
            print(f"   Processed {idx + 1}/{len(df_features)} files...")
    
    # Create DataFrame
    df_labels = pd.DataFrame(labels)
    
    # Show distribution
    print(f"\n📊 Label Distribution:")
    label_names = get_labels(config)
    for label_id in sorted(df_labels['difficulty_label'].unique()):
        count = (df_labels['difficulty_label'] == label_id).sum()
        percentage = (count / len(df_labels)) * 100
        label_name = label_names.get(label_id, f"Unknown-{label_id}")
        print(f"   {label_id}: {label_name:30s} → {count:5d} files ({percentage:5.1f}%)")
    
    # Save
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df_labels.to_csv(output_csv, index=False)
    print(f"\n✅ Saved {len(df_labels)} labels to: {output_csv}")
    print(f"\n{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(description="Automatic MIDI Difficulty Labeling")
    parser.add_argument(
        "--config",
        choices=["4_labels", "5_labels"],
        default="5_labels",
        help="Label configuration to use (default: 5_labels)"
    )
    parser.add_argument(
        "--features",
        type=Path,
        default=Path("data/processed/features_all.csv"),
        help="Path to features CSV file"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output CSV file (default: data/processed/labels/auto_{config}.csv)"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output file"
    )
    
    args = parser.parse_args()
    
    # Set default output path
    if args.output is None:
        args.output = Path(f"data/processed/labels/auto_{args.config}.csv")
    
    # Run auto-labeling
    auto_label_all(
        features_csv=args.features,
        output_csv=args.output,
        config=args.config,
        overwrite=args.overwrite
    )


if __name__ == "__main__":
    main()
