# Virtuoso Architect 🎹

Virtuoso Architect is an AI-powered system designed to analyze piano MIDI files, extract musical features, and classify them by technical difficulty. It combines automated rule-based labeling with a sophisticated manual labeling interface to create high-quality datasets for machine learning.

## 🚀 Features

- **Feature Extraction**: Analyzes MIDI files for chord density, polyphony, hand stretch, and more.
- **Auto-Labeling**: Rule-based classification engine supporting multiple configurations (4-Label & 5-Label).
- **Manual Labeling Tool**: Modern web interface for human experts to review and label pieces.
- **Machine Learning**: XGBoost-based difficulty classifier training pipeline.

## 🛠️ System Components

### 1. Labeling Configurations
The system works with two distinct difficulty configurations:
- **4-Labels (Balanced)**: Optimal for ML performance. IDs `[0, 1, 2, 3]`.
- **5-Labels (Granular)**: Includes specific "Multiple Voices" category. IDs `[0, 1, 2, 3, 4]`.

### 2. Project Structure
```
Virtuoso-Architect/
├── data/
│   ├── raw_midi/           # Source MIDI files
│   ├── processed/          # Extracted features (features_all.csv)
│   └── processed/labels/   # Generated labels (auto_4_labels.csv, etc.)
├── scripts/
│   ├── extract_features.py # Core feature extractor
│   ├── train_with_labels.py# Train ML model
│   └── evaluate_model.py   # Evaluate model performance
├── tools/
│   └── labeling/
│       ├── auto/           # Auto-labeling logic
│       ├── manual/         # Manual labeling web app
│       └── config.py       # Central configuration
└── README.md
```

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- Dependencies: `pandas`, `flask`, `scikit-learn`, `xgboost`, `mido`

### 1. Auto-Labeling
Generate labels automatically using predefined rules.
```bash
# Generate 5-label dataset (Standard)
python tools/labeling/auto/auto_label.py --config 5_labels

# Generate 4-label dataset (Simplified)
python tools/labeling/auto/auto_label.py --config 4_labels
```

### 2. Manual Labeling
Launch the web interface to label files manually.
```bash
# Start the server (Defaults to 5_labels)
python tools/labeling/manual/start_labeling.py
```
Open `http://localhost:5000` in your browser.

### 3. Model Training
Train the difficulty classifier using your labels.
```bash
python scripts/train_with_labels.py --labels auto_5_labels.csv
```

## 📊 Label Definitions

| ID | Category | Description |
|:--:|:---------|:------------|
| **0** | **Far Reach** | Wide hand spans and large interval jumps. |
| **1** | **Double Thirds** | Technical runs in thirds and rapid intervals. |
| **2** | **Advanced Chords** | Dense chord textures (9+ notes). |
| **3** | **Adv. Counterpoint** | Complex voice independence and polyrhythms. |
| **4** | **Multiple Voices** | (5-Label Only) Polyphonic complexity. |

## 🧪 Testing
To verify the integrity of the entire system:
```bash
python scripts/verify_system.py
```