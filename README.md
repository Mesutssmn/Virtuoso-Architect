# Virtuoso Architect: Technical Reference Manual 🎹

**Virtuoso Architect** is a comprehensive, AI-driven system designed to quantify the technical difficulty of piano compositions. It transforms subjective musical complexity into objective, quantifiable metrics using a sophisticated pipeline of Music Information Retrieval (MIR) algorithms and Machine Learning.

This documentation serves as a complete definition of the system architecture, design philosophy, and operational logic.

---

## 🛠️ Technology Stack & Rationale

We selected a robust, data-centric stack to ensure precision, speed, and scalability.

### Core Dependencies

| Library | Version | Purpose | Why we chose it? |
|:--------|:--------|:--------|:-----------------|
| **`mido`** | Latest | MIDI Parsing | The industry standard for Python MIDI handling. It allows low-level access to MIDI messages (Note On/Off) essential for calculating simultaneity and duration. |
| **`pandas`** | Latest | Data Manipulation | Used for handling large CSV datasets (`features_all.csv`). Its vectorized operations allow fast filtering and transformation of 10,000+ rows. |
| **`scikit-learn`** | Latest | ML Utilities | Provides robust tools for data splitting (`train_test_split`), metric calculation (Confusion Matrices), and preprocessing. |
| **`xgboost`** | Latest | Model Training | Gradient Boosting Framework. Chosen over Deep Learning (e.g., LSTM) because our features are **tabular/structured**. XGBoost offers superior performance and interpretability for this data type. |
| **`flask`** | Latest | Backend Server | A lightweight WSGI web application framework. Perfect for serving the Manual Labeling API with minimal overhead. |
| **`argparse`** | Std Lib | CLI Management | Ensures all scripts have professional, self-documenting command-line interfaces. |

---

## 📂 Project Structure & File Index

Every file in this repository has a specific, modular purpose.

### 1. Root Directory (`/`)
*   **`README.md`**: This documentation.
*   **`.gitignore`**: Excludes huge datasets and virtual environments from version control.

### 2. Data Pipeline (`data/`)
This directory follows a "Lake to Warehouse" philosophy.
*   **`data/raw_midi/`**: The immutable source of truth. Contains thousands of `.mid` or `.midi` files.
*   **`data/processed/features_all.csv`**: The "Feature Store". Every MIDI file is converted into a single row of mathematical features (Stretch, Density, etc.).
*   **`data/processed/labels/`**: The "Ground Truth" store. Example: `auto_5_labels.csv` contains the difficulty class for each file.

### 3. Core Scripts (`scripts/`)
Executable logic for the machine learning pipeline.
*   **`extract_features.py`**: The **ETL Engine**. It iterates through `raw_midi/`, parses note events, calculates statistics (e.g., "Max Chord Size"), and dumps them to `features_all.csv`.
*   **`train_with_labels.py`**: The **Model Trainer**. It merges Features + Labels, splits the data (80/20), trains an XGBoost Classifier, and saves the model.
*   **`evaluate_model.py`**: The **Auditor**. Loads a trained model and a test set to generate Classification Reports (Precision/Recall) and Confusion Matrices.
*   **`verify_system.py`**: The **Ci/CD Simulator**. Runs the entire pipeline from end-to-end to ensure system integrity.

### 4. Labeling Tools (`tools/labeling/`)
A dedicated module for generating Ground Truth data.
*   **`config.py`**: **THE BRAIN**. This single file defines the classification schema (4 vs 5 labels). Changing a threshold here updates the entire system.
*   **`auto/auto_label.py`**: **Rule Engine**. Applies music theory rules to features.
    *   *Example Rule:* "If `max_stretch > 25 semitones`, classify as `Far Reach`."
*   **`manual/labeling_server.py`**: **API Backend**. A Flask app that serves features and MIDI info to the frontend.
*   **`manual/labeling_interface.html`**: **The Frontend**. A Single Page Application (SPA) written in Vanilla JS/HTML/CSS. It consumes the API to let humans visually label music.

---

## 🧠 Architectural Decisions

### A. The "Single Source of Truth" Config
We faced a challenge where the Auto-Labeler and Manual UI drifted apart (e.g., one had 5 labels, the other 4).
*   **Solution:** We created `tools/labeling/config.py`.
*   **Effect:** Both the Python backend and the JavaScript frontend fetch their configuration from this file (via API). If you reorder labels in `config.py`, the UI buttons re-render automatically.

### B. Dual Classification Schema
We support two "Views" of the same data, handled via ID mapping strategies to maintain data continuity.

#### 1. The "Balanced" View (4-Labels)
Optimized for Machine Learning stability. Removes ambiguity.
*   **ID 0**: Far Reach
*   **ID 1**: Double Thirds
*   **ID 2**: Advanced Chords
*   **ID 3**: Advanced Counterpoint

#### 2. The "Granular" View (5-Labels)
Optimized for Musicological nuance.
*   **IDs 0-3**: Same as above (Perfect Consistency).
*   **ID 4**: Multiple Voices (Polyphony). ✨ *Added as an additive category.*

### C. Feature Extraction Logic
Instead of feeding raw MIDI audio (spectrograms) to the model, we extract high-level "Musical Concepts":
1.  **Max Stretch**: We calculate the interval between the lowest and highest note in a hand. >12 is a difficult span.
2.  **Polyphony**: We don't just count notes; we look for *sustained independent lines*.
3.  **Thirds Frequency**: We detect rapid successions of Major/Minor 3rds, indicative of specific technical etudes (e.g., Chopin Op. 25 No. 6).

---

## ⚡ detailed Usage Workflow

### Step 1: Feature Extraction
Convert raw audio data into math.
```bash
python scripts/extract_features.py
```
*Output: `data/processed/features_all.csv` (Rows: ~10k, Columns: 10)*

### Step 2: Label Generation
Create the "answer key" for the AI.

**Option A: Automated (Fast)**
Apply theoretical rules to generate thousands of labels instantly.
```bash
python tools/labeling/auto/auto_label.py --config 5_labels --overwrite
```

**Option B: Manual (Precise)**
Human-in-the-loop verification.
```bash
python tools/labeling/manual/start_labeling.py
```
*   Open browser at `http://localhost:5000`.
*   Use keyboard `0-4` to categorize nuances that rules might miss.

### Step 3: Model Training
Teach the AI to think like a pianist.
```bash
python scripts/train_with_labels.py --labels auto_5_labels.csv
```
The script uses XGBoost with `multi:softmax` objective function. It will output training accuracy logs.

### Step 4: System Verification
Run the integrated test suite to ensure all components talk to each other correctly.
```bash
python scripts/verify_system.py
```

---

## 🤝 Contribution Guidelines

1.  **Modify Logic**: To change how "Advanced Chords" are detected, edit the `AUTO_LABEL_THRESHOLDS` dictionary in `tools/labeling/config.py`. Do NOT hardcode values in scripts.
2.  **Add Features**: To add a new metric (e.g., "Arpeggio Speed"), modify `scripts/extract_features.py` and ensure the column name is added to the valid columns list.
3.  **UI Updates**: The frontend logic is in `labeling_interface.html`. It uses Vanilla JS for maximum compatibility. Avoid adding heavy frameworks (React/Vue) unless necessary.

---

*This system was architected to be a robust, professional-grade tool for Music AI research.*