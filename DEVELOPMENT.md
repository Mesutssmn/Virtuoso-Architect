# 🛠️ Development Guide - Building Virtuoso Architect from Scratch

This guide walks you through building the entire Virtuoso Architect system from the ground up.

---

## 📋 Prerequisites

- **Python 3.8+** installed
- **8GB+ RAM** (16GB recommended for large datasets)
- **Multi-core CPU** (4+ cores recommended)
- **Git** for version control

---

## 🚀 Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Virtuoso-Architect.git
cd Virtuoso-Architect
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `music21` - MIDI analysis
- `xgboost` - ML model
- `pandas` - Data processing
- `tqdm` - Progress bars
- `scikit-learn` - ML utilities

### 4. Download MIDI Dataset

**Option A: Giant MIDI Dataset (Recommended)**

1. Download from: https://github.com/bytedance/GiantMIDI-Piano
2. Extract to `data/raw/`

**Option B: Your Own MIDI Files**

Place your `.mid` files in `data/raw/` directory.

---

## 🎯 Building the System

### Step 1: Test Feature Extraction (Single File)

Test on a single MIDI file to verify setup:

```bash
.venv\Scripts\python.exe scripts/test_features.py
```

**Expected output:**
```
Testing feature extraction on first MIDI file...
✓ Found MIDI file: example.mid

Extracted Features:
  max_stretch: 24.0000
  max_chord_size: 4
  note_density: 8.5000
  ...
```

### Step 2: Quick Start (100-1000 Files)

Process a subset for initial testing:

```bash
.venv\Scripts\python.exe scripts/quick_start.py
```

**Options:**
- `1` - First 100 files (~5-10 minutes)
- `2` - First 1000 files (~20-30 minutes)
- `3` - All files (~2-4 hours)

**What it does:**
1. Extracts 10 features from each MIDI file
2. Saves to `data/processed/features.csv`
3. Trains XGBoost model with random labels (demo)
4. Saves model to `models/difficulty_classifier.pkl`
5. Tests on a sample file

### Step 3: Process Full Dataset

For production use with all files:

```bash
.venv\Scripts\python.exe scripts/quick_start_all_files.py
```

**Features:**
- ✅ Parallel processing (uses all CPU cores - 1)
- ✅ Auto-save every 100 files (`features_all_progress.csv`)
- ✅ Estimated time: 2-4 hours for 10,841 files
- ✅ Safe to Ctrl+C (last auto-save is kept)

**Output:**
- `data/processed/features_all.csv` - All extracted features
- `models/difficulty_classifier_full.pkl` - Trained model

---

## 📊 Analyzing Results

### Model Analysis

View feature importance and correlations:

```bash
.venv\Scripts\python.exe scripts/analyze_model.py
```

**Generates:**
- `models/feature_importance.png`
- `models/feature_correlation.png`
- `models/feature_distributions.png`

### Model Evaluation

Get detailed performance metrics:

```bash
.venv\Scripts\python.exe scripts/evaluate_model.py
```

**Outputs:**
- Accuracy, Precision, Recall, F1-Score
- Confusion matrix
- Confidence distribution
- Per-class performance

---

## 🎹 Using the System

### Analyze Single MIDI File

```bash
.venv\Scripts\python.exe src/main.py --midi_file "path/to/your/file.mid"
```

**Example output:**
```
🎹 TECHNICAL CLASSIFICATION
   Category: Far Reach
   Confidence: 43.19%

📊 EXTRACTED FEATURES (10 total)
   Max Stretch: 50.00 semitones
   Max Chord Size: 7 notes
   Note Density: 14.73 notes/sec
   ...
```

### With Custom Model

```bash
.venv\Scripts\python.exe src/main.py --midi_file "file.mid" --model "models/custom_model.pkl"
```

---

## 🔧 Advanced: Custom Model Training

### 1. Create Your Labels

Create `data/processed/labels.csv`:

```csv
midi_filename,difficulty_category
file1.mid,0
file2.mid,2
file3.mid,1
```

**Categories:**
- `0` - Far Reach
- `1` - Double Thirds
- `2` - Multiple Voices
- `3` - Advanced Chords
- `4` - Advanced Counterpoint

### 2. Train Custom Model

```python
import pandas as pd
from ml_engine.train import train_model

# Load features and labels
features = pd.read_csv("data/processed/features_all.csv")
labels = pd.read_csv("data/processed/labels.csv")

# Merge
df = features.merge(labels, on='midi_filename')

# Prepare data
feature_cols = [
    'max_stretch', 'max_chord_size', 'note_density',
    'left_hand_activity', 'avg_tempo', 'dynamic_range',
    'poly_voice_count', 'octave_jump_frequency',
    'thirds_frequency', 'polyrhythm_score'
]
X = df[feature_cols].values
y = df['difficulty_category'].values

# Train
model = train_model(X, y, model_save_path="models/my_model.pkl")
```

---

## 🐛 Troubleshooting

### Issue: "Out of Memory"

**Solution:** Reduce CPU cores in `quick_start.py`:

```python
# Line ~57
df_features = extract_features_batch(
    midi_files,
    output_csv=str(features_csv),
    n_jobs=3  # Reduce from default (cpu_count - 1)
)
```

### Issue: "music21 is slow"

**Solution:** This is normal. music21 is comprehensive but slow. The parallel processing helps significantly.

### Issue: "Model accuracy is low (20%)"

**Expected!** The demo uses random labels. For production:
1. Manually label your MIDI files
2. Create `labels.csv` with real categories
3. Retrain model
4. Expected accuracy: 60-80% with real labels

---

## 📁 Project Structure

```
Virtuoso-Architect/
├── src/
│   ├── main.py                    # Main analysis script
│   ├── ml_engine/
│   │   ├── feature_extract.py     # Feature extraction + parallel processing
│   │   └── train.py               # XGBoost training
│   └── rag_engine/                # Optional GPT-4o integration
├── scripts/
│   ├── quick_start.py            # Quick start (100-1000 files)
│   ├── quick_start_all_files.py  # Full dataset processing
│   ├── analyze_model.py          # Model analysis
│   ├── evaluate_model.py         # Model evaluation
│   └── test_features.py          # Feature testing
├── data/
│   ├── raw/                      # Your MIDI files
│   └── processed/                # Generated CSVs
├── models/                       # Trained models
└── docs/
    ├── USAGE.md                  # User guide
    ├── PARALLEL_PROCESSING.md    # Performance guide
    └── DEVELOPMENT.md            # This file
```

---

## 🎯 Development Workflow

### Typical Development Cycle

1. **Add MIDI files** to `data/raw/`
2. **Test extraction** with `test_features.py`
3. **Quick test** with `quick_start.py` (option 1: 100 files)
4. **Verify results** look reasonable
5. **Full processing** with `quick_start_all_files.py`
6. **Analyze model** with `analyze_model.py`
7. **Evaluate** with `evaluate_model.py`
8. **Use** with `main.py` for individual files

### Adding New Features

Edit `src/ml_engine/feature_extract.py`:

```python
def analyze_new_feature(stream):
    """
    Your new feature extraction logic.
    """
    # Your code here
    return feature_value

# Add to extract_features_from_midi():
features = {
    # ... existing features ...
    'new_feature': analyze_new_feature(stream)
}
```

Then update feature list in training scripts.

---

## 📈 Performance Optimization

### CPU Usage

**Default:** Uses `cpu_count - 1` cores

**Customize:**
```python
extract_features_batch(files, n_jobs=4)  # Use exactly 4 cores
```

### Auto-Save Interval

**Default:** Saves every 100 files

**Customize:**
```python
extract_features_batch(files, save_interval=50)  # Save every 50 files
```

### Memory Management

For very large datasets (>50,000 files):
- Process in batches of 5,000-10,000
- Use lower `n_jobs` value
- Monitor RAM usage

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Make changes
4. Test thoroughly
5. Commit (`git commit -m 'Add AmazingFeature'`)
6. Push (`git push origin feature/AmazingFeature`)
7. Open Pull Request

---

## 📝 Notes

### Current Limitations

- **Random labels:** Demo uses random difficulty categories
- **No RAG engine:** GPT-4o integration exists but is optional
- **Single-hand analysis:** Assumes standard piano (two hands)

### Future Improvements

- [ ] Manual labeling interface
- [ ] More sophisticated difficulty metrics
- [ ] Real-time MIDI analysis
- [ ] Web interface
- [ ] Support for other instruments

---

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review code comments

---

**Happy coding! 🎹🚀**
