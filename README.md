# Virtuoso Architect 🎹

**Virtuoso Architect** is an advanced AI-driven system designed to analyze, classify, and label piano MIDI compositions based on their technical difficulty. By bridging the gap between music theory and machine learning, it provides a robust pipeline for transforming raw MIDI data into structured, accurately labeled datasets suitable for training state-of-the-art proficiency models.

## 🌟 Key Features

### 1. Dual Labeling Ecosystem
The system uniquely supports two complementary labeling methodologies:
*   **Automated Rule-Based Labeling**: A high-speed engine that analyzes musical features (interval jumps, chord density, polyphony) to instantaneously classify thousands of files.
*   **Manual Expert Verification**: A modern, web-based interface allowing human experts to review, play, and correct labels with visual feedback on musical features.

### 2. Dynamic Configuration Engine
At the heart of the system is a **Central Configuration** (`config.py`) that drives all components. Changing a definition here automatically propagates to:
*   The Auto-labeling logic
*   The Manual Labeling UI (buttons & shortcuts)
*   The Machine Learning training pipeline

### 3. Flexible Classification Schemes
Users can seamlessly switch between two distinct difficulty granularities:
*   **4-Label System (Balanced)**: Optimized for ML model performance with balanced classes.
    *   `0: Far Reach` | `1: Double Thirds` | `2: Advanced Chords` | `3: Advanced Counterpoint`
*   **5-Label System (Granular)**: Includes specific separation for polyphonic texture.
    *   Adds `4: Multiple Voices` for distinct voice independence analysis.

### 4. Advanced Feature Extraction
The system extracts critical technical metrics from MIDI files, including:
*   **Hand Span/Stretch**: Detecting intervals greater than an octave.
*   **Polyrhythm Analysis**: Identifying complex rhythmic interplay between hands.
*   **Chord Density**: Measuring simultaneous note counts (up to 9+ notes).
*   **Voice Independence**: Tracking active polyphonic lines.

## 🏗️ System Architecture

The project is structured to ensure modularity and scalability:

```
Virtuoso-Architect/
├── data/
│   ├── raw_midi/           # Source compositions
│   └── processed/          # Extracted features & generated labels
├── scripts/
│   ├── extract_features.py # Core music theory analysis engine
│   ├── train_with_labels.py# XGBoost training pipeline
│   └── verify_system.py    # Automated end-to-end system verification
└── tools/
    └── labeling/
        ├── config.py       # SINGLE SOURCE OF TRUTH (Configuration)
        ├── auto/           # Automated classification logic
        └── manual/         # Flask + Vanilla JS Web Interface
```

## 🚀 Recent Enhancements

### User Interface & Experience
*   **Dynamic UI Generation**: The manual labeling interface now builds itself based on the selected configuration. Switching from 4 to 5 labels instantly updates the button layout and descriptions.
*   **0-Based Interaction**: To ensure consistency with Machine Learning standards, both the UI visualization and keyboard shortcuts strictly follow 0-based indexing (Keys `0-4`).

### Data Integrity
*   **Optimized ID Mapping**: We implemented a strict mapping strategy where IDs `0, 1, 2, 3` represent the exact same musical concepts across both configurations, with `4` being the additive category. This prevents data drift when switching modes.
*   **Centralized Logic**: Deprecated dispersed constants in favor of a single `config.py`, eliminating potential synchronization errors between frontend and backend.

## 🛠️ Installation & Usage

### Prerequisites
*   Python 3.8+
*   Pip dependencies: `pandas`, `flask`, `scikit-learn`, `xgboost`, `mido`

### 1. Automatic Labeling
Run the auto-labeler to process your entire dataset in seconds.
```bash
# Standard 5-label mode
python tools/labeling/auto/auto_label.py --config 5_labels

# ML-Optimized 4-label mode
python tools/labeling/auto/auto_label.py --config 4_labels
```

### 2. Manual Verification Interface
Launch the interactive web tool to review difficult cases.
```bash
python tools/labeling/manual/start_labeling.py
```
*   Access at: `http://localhost:5000`
*   Use Keyboard shortcuts **0-4** for rapid classification.
*   Use Arrow keys for navigation.

### 3. Training & Evaluation
Train the XGBoost classifier using your verified labels.
```bash
python scripts/train_with_labels.py --labels auto_5_labels.csv
python scripts/evaluate_model.py --labels auto_5_labels.csv
```

## 📊 Label Definitions

| ID | Category | Technical Criteria |
|:--:|:---------|:-------------------|
| **0** | **Far Reach** | Significant hand expansions, intervals > 12 semitones, rapid octave jumps. |
| **1** | **Double Thirds** | Fast parallel thirds, chromatic runs, high note density. |
| **2** | **Advanced Chords** | Vertical density > 9 notes, complex voicings, large simultaneous stretches. |
| **3** | **Adv. Counterpoint** | High left-hand activity, polyrhythms (3:2, 4:3), rhythmic independence. |
| **4** | **Multiple Voices** | *(5-Label Only)* 3+ distinct melodic lines, fugal textures, voice leading complexity. |

---
*Virtuoso Architect is built for musicologists and data scientists pushing the boundaries of Music IR (Information Retrieval).*