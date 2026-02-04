# Labels Directory

This directory contains all label datasets for MIDI difficulty classification.

## 📁 Files

### Active Label Sets
- **`auto_4_labels.csv`** - Auto-generated 4-category labels (10,841 files)
  - Generated: 2026-02-04
  - Categories: Far Reach, Double Thirds, Advanced Chords, Counterpoint
  - Distribution: 87% / 1% / 11% / <1%
  - Use: Recommended for production

- **`auto_5_labels.csv`** - Auto-generated 5-category labels (10,841 files)
  - Generated: 2026-02-04
  - Categories: Far Reach, Double Thirds, Multiple Voices, Advanced Chords, Counterpoint
  - Distribution: 87% / 1% / 0% / 11% / <1%
  - Use: Experimental (Multiple Voices needs tuning)

### Backup/Archive
- **`old_labels_backup.csv`** - OLD labels from previous system
  - ⚠️ DO NOT USE - Contains incorrect labels
  - From: Random label generation (0.2 accuracy)
  - Kept for reference only

### Progress Tracking
- **`labeling_progress.json`** - Manual labeling progress tracker

---

## 🚀 Usage

### Training with 4-Label Dataset
```bash
# Use auto_4_labels.csv (recommended)
.venv\Scripts\python.exe scripts\train_with_labels.py
```

### Training with 5-Label Dataset
```bash
# Use auto_5_labels.csv (experimental)
.venv\Scripts\python.exe scripts\train_with_labels.py
```

### Manual Labeling
```bash
# Start manual labeling interface
cd tools\labeling\manual
.venv\Scripts\python.exe start_labeling.py
```

---

## 📊 Label Format

All CSV files have the same structure:

```csv
midi_filename,difficulty_label,timestamp,confidence,method
example.mid,0,2026-02-04T17:35:21.563583,3,auto_4_labels
```

**Columns:**
- `midi_filename` - File identifier
- `difficulty_label` - Category (0-3 or 0-4)
- `timestamp` - When labeled
- `confidence` - Label confidence (1-5)
- `method` - How labeled (auto_4_labels, auto_5_labels, manual)

---

## ⚠️ Important Notes

1. **Never use `old_labels_backup.csv`** - It has random labels
2. **Default recommendation:** Use `auto_4_labels.csv` (better balance)
3. **For experiments:** Try `auto_5_labels.csv` + manual refinement
4. **Manual labels:** Will be saved as `manual.csv` (future)
