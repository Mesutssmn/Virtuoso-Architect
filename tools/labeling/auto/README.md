# Automatic MIDI Difficulty Labeling

Rule-based automatic labeling system for MIDI files.

## 🎯 Features

- **Dual Configuration**: Supports both 4 and 5 label systems
- **Feature-Based**: Uses 10 musical features for classification
- **Fast**: Labels 10k+ files in seconds
- **Configurable**: Easy to adjust thresholds

## 🚀 Usage

```bash
# From project root
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels

# Or 5 labels
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 5_labels

# Custom output
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels --output my_labels.csv

# Overwrite existing
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels --overwrite
```

## 📊 Algorithm

### 4-Label System

**Far Reach (0):**
- `max_stretch > 25` → +3 points
- `octave_jump_frequency > 0.15` → +2 points

**Double Thirds (1):**
- `thirds_frequency > 0.30` → +4 points
- `note_density > 8` → +1 point

**Advanced Chords (2):**
- `max_chord_size > 9` → +4 points
- `note_density > 10` → +2 points

**Advanced Counterpoint (3):**
- `poly_voice_count > 3` → +2 points
- `left_hand_activity > 0.35` → +2 points
- `polyrhythm_score > 0.25` → +2 points

### 5-Label System

Same as 4-label, plus:

**Multiple Voices (2):**
- `poly_voice_count > 3.5` → +3 points
- `left_hand_activity > 0.40` AND `max_chord_size < 8` → +2 points
- `polyrhythm_score > 0.15` → +2 points

## ⚙️ Customization

Edit thresholds in `../config.py`:

```python
AUTO_LABEL_THRESHOLDS = {
    "4_labels": {
        "far_reach": {
            "max_stretch": 25,  # Adjust this
            ...
        }
    }
}
```

## 📈 Performance

- **Speed**: ~10,000 files/second
- **Accuracy**: 60-70% (estimated)
- **Best for**: Initial baseline labels

## 💡 Tips

1. **Start with 4 labels** - More balanced distribution
2. **Review auto-labels** - Use manual tool to correct errors
3. **Tune thresholds** - Adjust based on your dataset
4. **Combine with manual** - Best of both worlds

## 🔍 Output Format

CSV with columns:
- `midi_filename` - File identifier
- `difficulty_label` - Category (0-3 or 0-4)
- `timestamp` - When labeled
- `confidence` - Always 3 for auto-labels
- `method` - `auto_4_labels` or `auto_5_labels`
