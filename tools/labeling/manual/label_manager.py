"""
Label Manager - Backend for Manual MIDI Labeling System
Handles CSV operations, progress tracking, and label validation.
"""

import pandas as pd
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from tools.labeling.config import get_labels, get_config_info, DEFAULT_CONFIG


class LabelManager:
    """Manages labels for MIDI files."""
    
    def __init__(self, features_csv: str, labels_csv: str, progress_file: str, config_name: str = DEFAULT_CONFIG):
        """
        Initialize Label Manager.
        
        Args:
            features_csv: Path to features CSV file
            labels_csv: Path to labels CSV file (will be created if doesn't exist)
            progress_file: Path to progress JSON file
            config_name: Label configuration name (e.g. "4_labels" or "5_labels")
        """
        self.features_csv = Path(features_csv)
        self.labels_csv = Path(labels_csv)
        self.progress_file = Path(progress_file)
        self.config_name = config_name
        
        # Load labels from config
        self.DIFFICULTY_LABELS = get_labels(config_name)
        self.config_info = get_config_info(config_name)
        
        # Load features
        self.features_df = pd.read_csv(self.features_csv)
        print(f"✓ Loaded {len(self.features_df)} MIDI files from features")
        
        # Load or create labels
        self._load_or_create_labels()
        
        # Load progress
        self.progress = self._load_progress()
    
    def _load_or_create_labels(self):
        """Load existing labels or create new labels CSV."""
        if self.labels_csv.exists():
            self.labels_df = pd.read_csv(self.labels_csv)
            print(f"✓ Loaded {len(self.labels_df)} existing labels")
        else:
            # Create empty labels dataframe
            self.labels_df = pd.DataFrame(columns=['midi_filename', 'difficulty_label', 'timestamp', 'confidence'])
            print("✓ Created new labels file")
    
    def _load_progress(self) -> Dict:
        """Load progress from JSON file."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                progress = json.load(f)
            print(f"✓ Loaded progress: {progress['labeled_count']}/{progress['total_count']} labeled")
            return progress
        else:
            # Create new progress
            progress = {
                'current_index': 0,
                'labeled_count': 0,
                'total_count': len(self.features_df),
                'last_updated': datetime.now().isoformat()
            }
            self._save_progress(progress)
            return progress
    
    def _save_progress(self, progress: Dict):
        """Save progress to JSON file."""
        progress['last_updated'] = datetime.now().isoformat()
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
    
    def get_current_file(self) -> Optional[Dict]:
        """
        Get current file to label.
        
        Returns:
            Dictionary with file info and features, or None if all labeled
        """
        current_idx = self.progress['current_index']
        
        if current_idx >= len(self.features_df):
            return None
        
        row = self.features_df.iloc[current_idx]
        
        # Get existing label if any
        existing_label = self.labels_df[
            self.labels_df['midi_filename'] == row['midi_filename']
        ]
        
        file_info = {
            'index': current_idx,
            'total': len(self.features_df),
            'filename': row['midi_filename'],
            'features': {
                'max_stretch': float(row['max_stretch']),
                'max_chord_size': int(row['max_chord_size']),
                'note_density': float(row['note_density']),
                'left_hand_activity': float(row['left_hand_activity']),
                'avg_tempo': float(row['avg_tempo']),
                'dynamic_range': float(row['dynamic_range']),
                'poly_voice_count': float(row['poly_voice_count']),
                'octave_jump_frequency': float(row['octave_jump_frequency']),
                'thirds_frequency': float(row['thirds_frequency']),
                'polyrhythm_score': float(row['polyrhythm_score'])
            },
            'existing_label': int(existing_label.iloc[0]['difficulty_label']) if len(existing_label) > 0 else None,
            'progress_percent': (self.progress['labeled_count'] / self.progress['total_count']) * 100
        }
        
        return file_info
    
    def save_label(self, filename: str, label: int, confidence: int = 5) -> bool:
        """
        Save a label for a file.
        
        Args:
            filename: MIDI filename
            label: Difficulty label (0-4)
            confidence: Confidence level (1-5, default 5)
            
        Returns:
            True if successful
        """
        # Validate label
        if label not in self.DIFFICULTY_LABELS:
            print(f"❌ Invalid label: {label}")
            return False
        
        # Check if label already exists
        existing = self.labels_df[self.labels_df['midi_filename'] == filename]
        
        if len(existing) > 0:
            # Update existing label
            self.labels_df.loc[self.labels_df['midi_filename'] == filename, 'difficulty_label'] = label
            self.labels_df.loc[self.labels_df['midi_filename'] == filename, 'timestamp'] = datetime.now().isoformat()
            self.labels_df.loc[self.labels_df['midi_filename'] == filename, 'confidence'] = confidence
        else:
            # Add new label
            new_label = pd.DataFrame([{
                'midi_filename': filename,
                'difficulty_label': label,
                'timestamp': datetime.now().isoformat(),
                'confidence': confidence
            }])
            self.labels_df = pd.concat([self.labels_df, new_label], ignore_index=True)
            self.progress['labeled_count'] += 1
        
        # Save to CSV
        self.labels_csv.parent.mkdir(parents=True, exist_ok=True)
        self.labels_df.to_csv(self.labels_csv, index=False)
        
        # Update progress
        self._save_progress(self.progress)
        
        return True
    
    def next_file(self) -> Optional[Dict]:
        """Move to next file and return its info."""
        self.progress['current_index'] += 1
        self._save_progress(self.progress)
        return self.get_current_file()
    
    def previous_file(self) -> Optional[Dict]:
        """Move to previous file and return its info."""
        if self.progress['current_index'] > 0:
            self.progress['current_index'] -= 1
            self._save_progress(self.progress)
        return self.get_current_file()
    
    def jump_to_index(self, index: int) -> Optional[Dict]:
        """Jump to specific index."""
        if 0 <= index < len(self.features_df):
            self.progress['current_index'] = index
            self._save_progress(self.progress)
            return self.get_current_file()
        return None
    
    def get_statistics(self) -> Dict:
        """Get labeling statistics."""
        if len(self.labels_df) == 0:
            return {
                'total_labeled': 0,
                'label_distribution': {},
                'completion_percent': 0.0
            }
        
        label_counts = self.labels_df['difficulty_label'].value_counts().to_dict()
        label_distribution = {
            self.DIFFICULTY_LABELS[int(k)]: int(v) 
            for k, v in label_counts.items()
        }
        
        return {
            'total_labeled': len(self.labels_df),
            'total_files': len(self.features_df),
            'label_distribution': label_distribution,
            'completion_percent': (len(self.labels_df) / len(self.features_df)) * 100
        }

    def get_config(self) -> Dict:
        """Get current configuration info."""
        return self.config_info


if __name__ == "__main__":
    # Test the label manager
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    features_csv = project_root / "data" / "processed" / "features_all.csv"
    labels_csv = project_root / "data" / "processed" / "labels.csv"
    progress_file = project_root / "data" / "processed" / "labeling_progress.json"
    
    manager = LabelManager(
        str(features_csv),
        str(labels_csv),
        str(progress_file)
    )
    
    # Get current file
    current = manager.get_current_file()
    if current:
        print(f"\nCurrent file: {current['filename']}")
        print(f"Progress: {current['index']}/{current['total']}")
        print(f"Features: {current['features']}")
    
    # Get statistics
    stats = manager.get_statistics()
    print(f"\nStatistics:")
    print(f"  Labeled: {stats['total_labeled']}/{stats['total_files']}")
    print(f"  Completion: {stats['completion_percent']:.2f}%")
    if stats['label_distribution']:
        print(f"  Distribution: {stats['label_distribution']}")
