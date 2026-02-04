# Labeling System

Organized system for labeling MIDI files with difficulty categories.

## 📁 Structure

```
labeling/
├── config.py              # Central label configuration
├── auto/                  # Automatic labeling
│   └── auto_label.py     # Rule-based auto-labeling
├── manual/                # Manual labeling interface
│   ├── label_manager.py
│   ├── labeling_server.py
│   ├── labeling_interface.html
│   └── start_labeling.py
└── LABELING_GUIDE.md      # Detailed labeling guide
```

## 🎯 Label Configurations

### 4-Label System (Balanced)
- **0: Far Reach** - Wide hand spans
- **1: Double Thirds** - Technical runs
- **2: Advanced Chords** - Dense textures
- **3: Advanced Counterpoint** - Voice independence

### 5-Label System (Granular)
- **0: Far Reach** - Wide hand spans
- **1: Double Thirds** - Technical runs
- **2: Multiple Voices** - Polyphonic complexity
- **3: Advanced Chords** - Dense textures
- **4: Advanced Counterpoint** - Advanced independence

## 🚀 Quick Start

### Automatic Labeling

```bash
# 4 labels (recommended for balanced dataset)
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels

# 5 labels (more granular)
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 5_labels
```

Output: `data/processed/labels/auto_{config}.csv`

### Manual Labeling

```bash
cd tools\labeling\manual
.venv\Scripts\python.exe start_labeling.py
```

Opens web interface at `http://localhost:5000`

## 📊 Current Label Distributions

### 4-Label Dataset
- Far Reach: 9,432 (87%)
- Double Thirds: 156 (1%)
- Advanced Chords: 1,246 (11%)
- Counterpoint: 7 (<1%)

### 5-Label Dataset
- Far Reach: 9,428 (87%)
- Double Thirds: 156 (1%)
- Multiple Voices: 0 (0%) ⚠️
- Advanced Chords: 1,246 (11%)
- Counterpoint: 11 (<1%)

**Note:** Multiple Voices category needs algorithm tuning or manual labeling.

## 🔧 Configuration

Edit `config.py` to:
- Add new label configurations
- Adjust auto-labeling thresholds
- Modify category definitions

## 📖 Documentation

See [LABELING_GUIDE.md](LABELING_GUIDE.md) for detailed category definitions and examples.
