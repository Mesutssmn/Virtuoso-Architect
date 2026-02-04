# Processed Data Directory

This directory contains processed feature data and labels for MIDI difficulty classification.

## 📁 Files

### Feature Data
- **`features_all.csv`** - Complete feature dataset (10,841 MIDI files)
  - 11 columns: `midi_filename` + 10 musical features
  - Features: max_stretch, max_chord_size, note_density, left_hand_activity, avg_tempo, dynamic_range, poly_voice_count, octave_jump_frequency, thirds_frequency, polyrhythm_score
  - Used by: Auto-labeling, Manual labeling, Training

### Label Data
- **`labels/`** - All label datasets (see [labels/README.md](labels/README.md))
  - `auto_4_labels.csv` - 4-category auto-generated labels ✅
  - `auto_5_labels.csv` - 5-category auto-generated labels ✅
  - `old_labels_backup.csv` - Old incorrect labels (DO NOT USE)

---

## 🔍 Feature Descriptions

| Feature | Description | Range |
|---------|-------------|-------|
| `max_stretch` | Maximum hand span in semitones | 0-40+ |
| `max_chord_size` | Largest chord (simultaneous notes) | 1-15+ |
| `note_density` | Average notes per second | 0-20+ |
| `left_hand_activity` | Left hand usage ratio | 0-1 |
| `avg_tempo` | Average tempo (BPM) | 40-200+ |
| `dynamic_range` | Velocity variation | 0-127 |
| `poly_voice_count` | Number of independent voices | 1-8+ |
| `octave_jump_frequency` | Frequency of large jumps | 0-1 |
| `thirds_frequency` | Frequency of third intervals | 0-1 |
| `polyrhythm_score` | Rhythmic complexity | 0-1 |

---

## 🚀 Usage

### Generate Features (if needed)
```bash
# Extract features from MIDI files
.venv\Scripts\python.exe src\feature_extraction\extract_features.py
```

### Use Features for Labeling
```bash
# Auto-labeling
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels

# Manual labeling
cd tools\labeling\manual
.venv\Scripts\python.exe start_labeling.py
```

### Train Model
```bash
# Uses features_all.csv + labels
.venv\Scripts\python.exe scripts\train_with_labels.py
```

---

## 📊 Data Quality

- **Total MIDI files:** 10,841
- **Feature completeness:** 100%
- **Missing values:** None
- **Data validation:** Passed

---

## ⚠️ Important Notes

1. **Only use `features_all.csv`** - It's the complete dataset
2. **Features are normalized** - Ready for ML training
3. **Consistent with labels** - Same 10,841 files
4. **Regenerate if needed** - Run feature extraction script
