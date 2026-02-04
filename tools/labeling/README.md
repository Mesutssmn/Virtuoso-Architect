# Labeling System 🏷️

This directory contains the core logic for assigning difficulty labels to MIDI files. The system is designed to correct the "Single Folder" issue by providing structured, reliable labeling methods.

## Overview
We provide two complementary approaches to labeling:
1.  **Auto Labeling (`auto/`)**: Fast, rule-based initial labeling based on extracted features.
2.  **Manual Labeling (`manual/`)**: Expert human verification via a web interface.

Both systems rely on a **Central Configuration** (`config.py`) to ensuring consistency across the entire project.

## Configuration Modes through `config.py`

You can switch between two difficulty granularities. The system automatically adapts ID mappings.

### 🌟 4-Labels (Balanced)
Best for training machine learning models with balanced classes.
- **IDs**: `0, 1, 2, 3`
- **Labels**: Far Reach, Double Thirds, Advanced Chords, Advanced Counterpoint.

### 🌟 5-Labels (Granular)
Best for detailed musicological analysis.
- **IDs**: `0, 1, 2, 3, 4`
- **Labels**: Same as above, plus **Multiple Voices (ID 4)**.

## Directory Layout
```
tools/labeling/
├── config.py           # MASTER CONFIG - Defines all labels and thresholds
├── auto/               # Auto-labeling scripts
│   ├── auto_label.py
│   └── README.md
└── manual/             # Manual labeling application
    ├── labeling_server.py
    ├── labeling_interface.html
    └── README.md
```

## Usage
The central config ensures that if you change a definition in `config.py`, it propagates to:
- The Auto-Labeling rules
- The Manual Labeling UI buttons
- The Training pipeline class names
