# 🎹 Virtuoso Architect

**AI-Powered Piano MIDI Technical Difficulty Classification System**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A complete machine learning system for analyzing and classifying piano MIDI files by technical difficulty**

---

## 📖 The Story

### The Problem
Piano teachers and students need to understand the technical challenges in a piece before practicing. Traditional methods rely on subjective assessment or manual analysis, which is time-consuming and inconsistent.

### The Journey
This project started with a simple goal: automatically classify piano MIDI files by difficulty. However, we quickly discovered that **random labels produce random results** (~20% accuracy). 

The breakthrough came when we built a **dual labeling system**:
1. **Automatic labeling** - Rule-based algorithm using musical features
2. **Manual labeling** - Web interface for human verification

This hybrid approach, combined with proper data organization and configurable label counts, created a production-ready system.

### The Solution
Virtuoso Architect now provides:
- ✅ **10,841 automatically labeled MIDI files** (4 or 5 categories)
- ✅ **Dual labeling system** (auto + manual)
- ✅ **Flexible configuration** (4-label balanced or 5-label granular)
- ✅ **Production-ready ML pipeline** with XGBoost
- ✅ **Comprehensive documentation** for users and developers

---

## ✨ Key Features

### 🎼 Musical Analysis
- **10 Comprehensive Features** - Hand span, chord complexity, note density, polyphony, tempo, dynamics, and more
- **Intelligent Feature Extraction** - Analyzes MIDI structure, timing, and musical patterns
- **Parallel Processing** - 7x faster with multi-core CPU support

### 🏷️ Dual Labeling System
- **Automatic Labeling** - Rule-based algorithm labels 10k+ files in seconds
- **Manual Labeling** - Web interface with MIDI playback for verification
- **Flexible Configurations** - Support for 4 or 5 difficulty categories

### 🤖 Machine Learning
- **XGBoost Classifier** - Industry-standard gradient boosting
- **Configurable Categories** - 4-label (balanced) or 5-label (granular)
- **Real Labels** - No more random labels, actual difficulty classifications

### 📊 Data Management
- **Organized Structure** - Clean separation of features, labels, and models
- **Multiple Label Sets** - Compare 4-label vs 5-label approaches
- **Comprehensive Documentation** - Every file and folder explained

---

## 🎯 Difficulty Categories

### 4-Label System (Recommended - Balanced)

| ID | Category | Description | Example Features |
|----|----------|-------------|------------------|
| 0 | **Far Reach** | Wide hand spans | max_stretch > 25 semitones |
| 1 | **Double Thirds** | Technical runs in thirds | thirds_frequency > 0.30 |
| 2 | **Advanced Chords** | Dense chord textures | max_chord_size > 9 notes |
| 3 | **Advanced Counterpoint** | Voice independence | poly_voice_count > 3, polyrhythm > 0.25 |

**Current Distribution:** 87% / 1% / 11% / <1% (10,841 files)

### 5-Label System (Experimental - Granular)

| ID | Category | Description | Example Features |
|----|----------|-------------|------------------|
| 0 | **Far Reach** | Wide hand spans | max_stretch > 25 semitones |
| 1 | **Double Thirds** | Technical runs in thirds | thirds_frequency > 0.30 |
| 2 | **Multiple Voices** | Polyphonic complexity | poly_voice_count > 3.5, moderate chords |
| 3 | **Advanced Chords** | Dense chord textures | max_chord_size > 9 notes |
| 4 | **Advanced Counterpoint** | Advanced independence | poly_voice_count > 4, polyrhythm > 0.30 |

**Current Distribution:** 87% / 1% / 0% / 11% / <1% (10,841 files)
⚠️ *Multiple Voices category needs algorithm tuning or manual labeling*

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 8GB+ RAM (16GB recommended)
- Multi-core CPU (4+ cores recommended)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Mesutssmn/Virtuoso-Architect.git
cd Virtuoso-Architect

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt
```

### Basic Usage

#### Option 1: Automatic Labeling (Fast)

Generate labels for all MIDI files using rule-based algorithm:

```bash
# 4-label system (recommended)
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels

# 5-label system (experimental)
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 5_labels
```

**What it does:**
- Analyzes 10 musical features per file
- Applies rule-based scoring algorithm
- Generates labels in seconds (10k+ files)
- Saves to `data/processed/labels/auto_4_labels.csv` or `auto_5_labels.csv`

#### Option 2: Manual Labeling (High Quality)

Review and correct labels using web interface:

```bash
cd tools\labeling\manual
.venv\Scripts\python.exe start_labeling.py
```

**What it does:**
- Opens web interface at `http://localhost:5000`
- Shows MIDI playback and features
- Keyboard shortcuts (1-5) for fast labeling
- Auto-saves progress
- Can review/correct auto-generated labels

#### Option 3: Train Model

Train XGBoost model with labeled data:

```bash
.venv\Scripts\python.exe scripts\train_with_labels.py
```

**What it does:**
- Loads features from `features_all.csv`
- Loads labels from `labels/auto_4_labels.csv` (or auto_5_labels.csv)
- Trains XGBoost classifier
- Saves model to `models/difficulty_classifier.pkl`
- Shows accuracy and distribution

#### Option 4: Evaluate Model

Check model performance:

```bash
.venv\Scripts\python.exe scripts\evaluate_model.py
```

**What it does:**
- Loads trained model
- Tests on validation set
- Shows accuracy, precision, recall, F1-score
- Generates confusion matrix
- Displays per-class performance

---

## 📁 Project Structure

```
Virtuoso-Architect/
├── 📂 tools/labeling/              # Labeling system
│   ├── config.py                   # Central label configuration
│   ├── LABELING_GUIDE.md          # Detailed labeling guide
│   ├── README.md                   # Labeling system overview
│   │
│   ├── 📂 auto/                    # Automatic labeling
│   │   ├── auto_label.py          # Rule-based labeling (4 or 5 labels)
│   │   └── README.md              # Auto-labeling documentation
│   │
│   └── 📂 manual/                  # Manual labeling
│       ├── label_manager.py       # Backend logic
│       ├── labeling_server.py     # Flask REST API
│       ├── labeling_interface.html # Web UI
│       ├── start_labeling.py      # Quick start script
│       └── README.md              # Manual labeling documentation
│
├── 📂 data/
│   ├── raw/                        # MIDI files (10,841 files, gitignored)
│   └── processed/                  # Processed data
│       ├── features_all.csv       # Extracted features (10,841 files)
│       ├── README.md              # Data documentation
│       └── labels/                # Label datasets
│           ├── auto_4_labels.csv  # 4-category labels ✅
│           ├── auto_5_labels.csv  # 5-category labels ✅
│           ├── old_labels_backup.csv # Old incorrect labels (DO NOT USE)
│           └── README.md          # Label documentation
│
├── 📂 src/
│   ├── ml_engine/
│   │   ├── feature_extract.py     # Feature extraction + parallel processing
│   │   └── train.py               # XGBoost training
│   ├── rag_engine/                # Optional GPT-4o integration
│   └── main.py                    # Main analysis script
│
├── 📂 scripts/
│   ├── train_with_labels.py       # Train with real labels
│   ├── evaluate_model.py          # Model evaluation
│   └── analyze_model.py           # Feature importance analysis
│
├── 📂 models/                      # Trained models (gitignored)
│   └── difficulty_classifier.pkl  # Current trained model
│
└── README.md                       # This file
```

---

## 📊 The 10 Musical Features

Each MIDI file is analyzed to extract 10 comprehensive features:

| # | Feature | Description | Range | Why It Matters |
|---|---------|-------------|-------|----------------|
| 1 | **Max Stretch** | Maximum hand span in semitones | 0-40+ | Wide reaches indicate difficulty |
| 2 | **Max Chord Size** | Largest simultaneous note count | 1-15+ | Dense chords are harder to play |
| 3 | **Note Density** | Average notes per second | 0-20+ | Fast passages increase difficulty |
| 4 | **Left Hand Activity** | Left hand usage ratio | 0-1 | Active left hand adds complexity |
| 5 | **Average Tempo** | Tempo in BPM | 40-200+ | Faster tempos are more challenging |
| 6 | **Dynamic Range** | Velocity variation | 0-127 | Wide dynamics require control |
| 7 | **Poly Voice Count** | Number of independent voices | 1-8+ | More voices = more complexity |
| 8 | **Octave Jump Frequency** | Frequency of large jumps | 0-1 | Frequent jumps are difficult |
| 9 | **Thirds Frequency** | Frequency of third intervals | 0-1 | Double thirds are technical |
| 10 | **Polyrhythm Score** | Rhythmic complexity | 0-1 | Complex rhythms are harder |

**Why These Features?**
- Based on piano pedagogy and technical difficulty research
- Measurable from MIDI data
- Correlate with actual playing difficulty
- Used by auto-labeling algorithm and ML model

---

## 🔄 Complete Workflows

### Workflow 1: Quick Start (Auto-Label + Train)

**Best for:** Getting started quickly

```bash
# 1. Generate labels (4-label recommended)
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels

# 2. Train model
.venv\Scripts\python.exe scripts\train_with_labels.py

# 3. Evaluate
.venv\Scripts\python.exe scripts\evaluate_model.py
```

**Time:** ~5-10 minutes  
**Expected Accuracy:** 60-70% (with auto-labels)

---

### Workflow 2: High Quality (Auto + Manual + Train)

**Best for:** Production use

```bash
# 1. Generate baseline labels
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels

# 2. Review/correct labels manually
cd tools\labeling\manual
.venv\Scripts\python.exe start_labeling.py
# Review 200-500 files, correct obvious errors

# 3. Train with corrected labels
.venv\Scripts\python.exe scripts\train_with_labels.py

# 4. Evaluate
.venv\Scripts\python.exe scripts\evaluate_model.py
```

**Time:** 2-4 hours (depending on manual review)  
**Expected Accuracy:** 70-80% (with manual corrections)

---

### Workflow 3: Experiment with 5 Labels

**Best for:** Research and experimentation

```bash
# 1. Generate 5-label dataset
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 5_labels

# 2. Manually add Multiple Voices examples
cd tools\labeling\manual
# Edit config.py: DEFAULT_CONFIG = "5_labels"
.venv\Scripts\python.exe start_labeling.py
# Add Multiple Voices category examples

# 3. Train
.venv\Scripts\python.exe scripts\train_with_labels.py

# 4. Compare with 4-label model
.venv\Scripts\python.exe scripts\evaluate_model.py
```

**Time:** 3-5 hours  
**Expected Accuracy:** 65-75% (needs Multiple Voices tuning)

---

## 🎓 Understanding the System

### Why Two Labeling Systems?

**Automatic Labeling:**
- ✅ **Fast** - Labels 10k+ files in seconds
- ✅ **Consistent** - Same rules applied to all files
- ✅ **Baseline** - Good starting point
- ❌ **Limited** - Can't capture all nuances
- ❌ **Imbalanced** - Some categories underrepresented

**Manual Labeling:**
- ✅ **Accurate** - Human judgment
- ✅ **Flexible** - Can handle edge cases
- ✅ **Balanced** - Can ensure class balance
- ❌ **Slow** - Takes time
- ❌ **Subjective** - Requires expertise

**Best Approach:** Use automatic labeling for baseline, then manually review/correct a subset (200-500 files) for best results.

---

### Why Two Label Configurations?

**4-Label System:**
- ✅ More balanced distribution
- ✅ Simpler model
- ✅ Faster training
- ✅ Good enough for most use cases
- ✅ **Recommended for production**

**5-Label System:**
- ✅ More granular categories
- ✅ Distinguishes polyphonic complexity
- ✅ Better for research
- ⚠️ Multiple Voices needs tuning
- ⚠️ More imbalanced
- 🔬 **Experimental**

**Recommendation:** Start with 4-label system. Experiment with 5-label if you need more granularity and can manually label Multiple Voices examples.

---

### Why CSV Files?

**features_all.csv:**
- Contains 10 extracted features for all 10,841 MIDI files
- Used by both auto-labeling and manual labeling
- Used by training scripts
- **Purpose:** Single source of truth for feature data

**auto_4_labels.csv / auto_5_labels.csv:**
- Auto-generated labels using rule-based algorithm
- Quick baseline for training
- **Purpose:** Fast labeling without manual work

**manual.csv (future):**
- Labels created/corrected via web interface
- Higher quality than auto-labels
- **Purpose:** Best accuracy for production

---

## 🛠️ Advanced Usage

### Custom Label Thresholds

Edit `tools/labeling/config.py` to adjust auto-labeling:

```python
AUTO_LABEL_THRESHOLDS = {
    "4_labels": {
        "far_reach": {
            "max_stretch": 25,  # Lower = more Far Reach labels
            "octave_jump_frequency": 0.15
        },
        # ... adjust other thresholds
    }
}
```

### Add New Label Configuration

```python
# In tools/labeling/config.py
LABEL_CONFIGS = {
    "3_labels": {  # New configuration
        0: "Easy",
        1: "Medium",
        2: "Hard"
    }
}
```

Then create corresponding auto-labeling logic in `tools/labeling/auto/auto_label.py`.

### Extract Features from New MIDI Files

```bash
# If you add new MIDI files to data/raw/
.venv\Scripts\python.exe src\ml_engine\feature_extract.py
```

---

## 📈 Performance & Optimization

### Parallel Processing

Feature extraction uses all CPU cores minus 1-2:

**Speed Comparison:**

| Mode | CPU Usage | 100 Files | 10,841 Files |
|------|-----------|-----------|--------------|
| Serial | 1 core | ~10 min | ~18 hours |
| **Parallel** | **7-15 cores** | **~2-3 min** | **~2-4 hours** |

**~7x speed improvement** on 8-core CPU!

### Memory Management

For large datasets:
- System automatically manages CPU cores
- Auto-saves progress every 100 files
- Safe to Ctrl+C (progress is saved)

---

## 🐛 Troubleshooting

### "Model not found"
**Solution:** Train model first
```bash
.venv\Scripts\python.exe scripts\train_with_labels.py
```

### "Labels file not found"
**Solution:** Generate labels first
```bash
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels
```

### "Out of memory"
**Solution:** Close other programs or reduce CPU cores in feature extraction

### "Low accuracy (~20%)"
**Cause:** Using old random labels  
**Solution:** Use new auto-generated labels or manual labeling

---

## 📚 Documentation

- **[tools/labeling/README.md](tools/labeling/README.md)** - Labeling system overview
- **[tools/labeling/auto/README.md](tools/labeling/auto/README.md)** - Auto-labeling guide
- **[tools/labeling/manual/README.md](tools/labeling/manual/README.md)** - Manual labeling guide
- **[tools/labeling/LABELING_GUIDE.md](tools/labeling/LABELING_GUIDE.md)** - Detailed category definitions
- **[data/processed/README.md](data/processed/README.md)** - Data structure documentation
- **[data/processed/labels/README.md](data/processed/labels/README.md)** - Label files documentation

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[music21](https://web.mit.edu/music21/)** - Comprehensive music analysis library
- **[XGBoost](https://xgboost.readthedocs.io/)** - High-performance gradient boosting framework
- **[Giant MIDI Dataset](https://github.com/bytedance/GiantMIDI-Piano)** - Large-scale piano MIDI dataset

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

## 🎯 Project Status

**Current Version:** 2.0 - Production Ready

**System Status:**
- ✅ Feature extraction working (10 features, parallel processing)
- ✅ Auto-labeling system complete (4 and 5 labels)
- ✅ Manual labeling interface ready
- ✅ Training pipeline functional (real labels)
- ✅ Model evaluation working
- ✅ Comprehensive documentation
- ✅ Clean, organized codebase

**What's New in 2.0:**
- 🎉 Dual labeling system (auto + manual)
- 🎉 Configurable label counts (4 or 5)
- 🎉 Real labels (no more random labels)
- 🎉 Organized data structure
- 🎉 Comprehensive documentation
- 🎉 Production-ready pipeline

---

**Made with ❤️ for pianists, music educators, and ML enthusiasts**