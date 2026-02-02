"""
Enhanced Feature Extraction Engine for MIDI Files
Extracts 10 comprehensive technical difficulty features.
"""

import music21
import numpy as np
from pathlib import Path
import warnings

# Disable warnings for cleaner output
warnings.filterwarnings('ignore')
music21.environment.UserSettings()['warnings'] = 0


def analyze_hand_span(stream):
    """
    Analyze maximum hand span required (max_stretch).
    Returns maximum interval in semitones.
    """
    max_stretch = 0
    notes = stream.flatten().notes
    
    for element in notes:
        if isinstance(element, music21.chord.Chord):
            pitches = [p.midi for p in element.pitches]
            if len(pitches) >= 2:
                stretch = max(pitches) - min(pitches)
                max_stretch = max(max_stretch, stretch)
    
    return float(max_stretch)


def analyze_max_chord_size(stream):
    """
    Analyze maximum simultaneous notes (max_chord_size).
    """
    max_chord_size = 0
    notes = stream.flatten().notes
    
    for element in notes:
        if isinstance(element, music21.chord.Chord):
            chord_size = len(element.pitches)
            max_chord_size = max(max_chord_size, chord_size)
    
    return int(max_chord_size)


def analyze_note_density(stream):
    """
    Calculate notes per second (note_density).
    """
    notes = stream.flatten().notesAndRests
    
    total_notes = 0
    for element in notes:
        if isinstance(element, music21.chord.Chord):
            total_notes += len(element.pitches)
        elif isinstance(element, music21.note.Note):
            total_notes += 1
    
    duration = stream.duration.quarterLength
    
    # Assume 120 BPM default
    tempo = 120
    metronomes = stream.flatten().getElementsByClass(music21.tempo.MetronomeMark)
    if metronomes:
        tempo = metronomes[0].number
    
    duration_seconds = (duration / tempo) * 60
    
    if duration_seconds > 0:
        return float(total_notes / duration_seconds)
    return 0.0


def analyze_left_hand_activity(stream):
    """
    Measure left hand activity (notes below middle C).
    Returns ratio of left hand notes to total notes.
    """
    notes = stream.flatten().notes
    total_notes = 0
    left_hand_notes = 0
    
    middle_c = 60  # MIDI number for middle C
    
    for element in notes:
        if isinstance(element, music21.chord.Chord):
            for pitch in element.pitches:
                total_notes += 1
                if pitch.midi < middle_c:
                    left_hand_notes += 1
        elif isinstance(element, music21.note.Note):
            total_notes += 1
            if element.pitch.midi < middle_c:
                left_hand_notes += 1
    
    if total_notes > 0:
        return float(left_hand_notes / total_notes)
    return 0.0


def analyze_tempo(stream):
    """
    Extract average tempo (avg_tempo).
    """
    metronomes = stream.flatten().getElementsByClass(music21.tempo.MetronomeMark)
    
    if metronomes:
        tempos = [m.number for m in metronomes]
        return float(np.mean(tempos))
    
    return 120.0  # Default tempo


def analyze_dynamic_range(stream):
    """
    Measure dynamic range (dynamic_range).
    Returns range of dynamics from pp to ff.
    """
    dynamics = stream.flatten().getElementsByClass(music21.dynamics.Dynamic)
    
    if not dynamics:
        return 0.0
    
    # Map dynamics to numeric values
    dynamic_map = {
        'ppp': 1, 'pp': 2, 'p': 3, 'mp': 4, 'mf': 5, 'f': 6, 'ff': 7, 'fff': 8
    }
    
    dynamic_values = []
    for dyn in dynamics:
        if dyn.value in dynamic_map:
            dynamic_values.append(dynamic_map[dyn.value])
    
    if dynamic_values:
        return float(max(dynamic_values) - min(dynamic_values))
    
    return 0.0


def analyze_polyphony(stream):
    """
    Count average number of simultaneous voices (poly_voice_count).
    """
    # Count parts/voices
    parts = stream.parts
    
    if parts:
        return float(len(parts))
    
    # If no parts, estimate from note density
    notes = stream.flatten().notes
    simultaneous_notes = []
    
    for element in notes:
        if isinstance(element, music21.chord.Chord):
            simultaneous_notes.append(len(element.pitches))
        else:
            simultaneous_notes.append(1)
    
    if simultaneous_notes:
        return float(np.mean(simultaneous_notes))
    
    return 1.0


def analyze_octave_jumps(stream):
    """
    Measure frequency of octave jumps (octave_jump_frequency).
    Returns ratio of octave+ jumps to total intervals.
    """
    notes_list = []
    for element in stream.flatten().notes:
        if isinstance(element, music21.note.Note):
            notes_list.append(element.pitch.midi)
        elif isinstance(element, music21.chord.Chord):
            # Use highest note of chord
            notes_list.append(max(p.midi for p in element.pitches))
    
    if len(notes_list) < 2:
        return 0.0
    
    octave_jumps = 0
    total_intervals = len(notes_list) - 1
    
    for i in range(len(notes_list) - 1):
        interval = abs(notes_list[i+1] - notes_list[i])
        if interval >= 12:  # Octave or more
            octave_jumps += 1
    
    if total_intervals > 0:
        return float(octave_jumps / total_intervals)
    
    return 0.0


def analyze_thirds(stream):
    """
    Detect frequency of thirds (thirds_frequency).
    Returns ratio of third intervals to total intervals.
    """
    notes_list = []
    for element in stream.flatten().notes:
        if isinstance(element, music21.note.Note):
            notes_list.append(element.pitch.midi)
    
    if len(notes_list) < 2:
        return 0.0
    
    thirds_count = 0
    total_intervals = len(notes_list) - 1
    
    for i in range(len(notes_list) - 1):
        interval = abs(notes_list[i+1] - notes_list[i]) % 12
        if interval in [3, 4]:  # Minor third (3) or major third (4)
            thirds_count += 1
    
    if total_intervals > 0:
        return float(thirds_count / total_intervals)
    
    return 0.0


def analyze_polyrhythm(stream):
    """
    Detect polyrhythmic complexity (polyrhythm_score).
    Returns score based on rhythmic diversity.
    """
    notes = stream.flatten().notes
    
    durations = []
    for element in notes:
        if hasattr(element, 'quarterLength'):
            durations.append(element.quarterLength)
    
    if not durations:
        return 0.0
    
    # Count unique duration values
    unique_durations = len(set(durations))
    
    # Normalize by total notes
    if len(durations) > 0:
        return float(unique_durations / len(durations))
    
    return 0.0


def extract_features_from_midi(midi_path):
    """
    Extract all 10 technical difficulty features from a MIDI file.
    
    Args:
        midi_path (str): Path to MIDI file
        
    Returns:
        dict: Dictionary of 10 features
    """
    try:
        # Parse MIDI file with faster method
        stream = music21.converter.parse(midi_path, forceSource=True, storePickle=False)
        
        # Extract all features
        features = {
            'max_stretch': analyze_hand_span(stream),
            'max_chord_size': analyze_max_chord_size(stream),
            'note_density': analyze_note_density(stream),
            'left_hand_activity': analyze_left_hand_activity(stream),
            'avg_tempo': analyze_tempo(stream),
            'dynamic_range': analyze_dynamic_range(stream),
            'poly_voice_count': analyze_polyphony(stream),
            'octave_jump_frequency': analyze_octave_jumps(stream),
            'thirds_frequency': analyze_thirds(stream),
            'polyrhythm_score': analyze_polyrhythm(stream)
        }
        
        return features
        
    except KeyboardInterrupt:
        raise
    except Exception as e:
        # Skip corrupted or problematic files
        return None


def extract_features_batch(midi_files, output_csv=None, n_jobs=None):
    """
    Extract features from multiple MIDI files using parallel processing.
    
    Args:
        midi_files (list): List of MIDI file paths
        output_csv (str, optional): Path to save features CSV
        n_jobs (int, optional): Number of parallel jobs. 
                               None = use all CPUs - 1 (to keep system responsive)
        
    Returns:
        pd.DataFrame: DataFrame with features for all files
    """
    import pandas as pd
    from tqdm import tqdm
    import multiprocessing as mp
    import os
    from pathlib import Path
    
    # Determine number of workers
    if n_jobs is None:
        # Use all CPUs minus 1 to keep system responsive
        n_jobs = max(1, mp.cpu_count() - 1)
    
    print(f"  💻 Using {n_jobs} CPU cores (out of {mp.cpu_count()} available)")
    print(f"  📊 Processing {len(midi_files)} MIDI files...")
    
    # Process files in parallel
    results = []
    
    try:
        # Use multiprocessing Pool
        with mp.Pool(processes=n_jobs) as pool:
            # Process files with progress bar
            for features in tqdm(
                pool.imap(_extract_features_worker, midi_files),
                total=len(midi_files),
                desc="Extracting features"
            ):
                if features:
                    results.append(features)
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user (Ctrl+C)")
        print(f"  📊 Saving {len(results)} processed files before exit...")
        
        # Save partial results
        if results and output_csv:
            df_partial = pd.DataFrame(results)
            partial_path = output_csv.replace('.csv', '_partial.csv')
            os.makedirs(os.path.dirname(output_csv), exist_ok=True)
            df_partial.to_csv(partial_path, index=False)
            print(f"  ✓ Partial results saved to {partial_path}")
            print(f"  ✓ {len(results)} files saved successfully!")
            return df_partial
        else:
            print("  ❌ No results to save")
            raise
    
    df = pd.DataFrame(results)
    
    if output_csv:
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        df.to_csv(output_csv, index=False)
        print(f"\n  ✓ Saved features to {output_csv}")
    
    return df


def _extract_features_worker(midi_path):
    """
    Worker function for parallel processing.
    Extracts features from a single MIDI file.
    
    Args:
        midi_path (str): Path to MIDI file
        
    Returns:
        dict: Features dictionary with filename
    """
    from pathlib import Path # Import Path here for the worker function
    features = extract_features_from_midi(midi_path)
    if features:
        features['midi_filename'] = Path(midi_path).name
        return features
    return None


if __name__ == "__main__":
    # Test feature extraction
    import sys
    
    if len(sys.argv) > 1:
        midi_path = sys.argv[1]
        print(f"Extracting features from: {midi_path}")
        features = extract_features_from_midi(midi_path)
        
        if features:
            print("\nExtracted Features:")
            for key, value in features.items():
                print(f"  {key}: {value:.4f}")
    else:
        print("Usage: python feature_extract.py <path_to_midi_file>")
