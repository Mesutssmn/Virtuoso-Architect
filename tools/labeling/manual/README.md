# Manual MIDI Difficulty Labeling

**Web-based interface for manually labeling and reviewing piano MIDI files**

---

## 📖 The Story

### Why Manual Labeling?

Automatic labeling is fast but imperfect. It produces:
- ✅ Quick baseline (10k+ files in seconds)
- ❌ Imbalanced distribution (87% one category)
- ❌ Can't capture all nuances
- ❌ Some categories underrepresented

**Solution:** Manual review and correction for higher accuracy.

### The Challenge

Creating a labeling interface that:
- Shows MIDI playback (hear the piece)
- Displays all 10 features (see the data)
- Fast keyboard shortcuts (efficient workflow)
- Saves progress automatically (resume anytime)
- Works with both 4 and 5-label configurations

### The Solution

We built a modern web interface with:
- **Flask REST API** - Serves data and handles saves
- **HTML/CSS/JS Frontend** - Clean, responsive UI
- **MIDI Playback** - Listen while labeling
- **Feature Visualization** - See all 10 features
- **Progress Tracking** - Auto-save and resume
- **Keyboard Shortcuts** - Fast labeling (1-5 keys)

**Result:** Professional labeling tool for high-quality labels!

---

## 🎯 Features

### 🎵 MIDI Playback
- Play/pause MIDI directly in browser
- Hear the piece while labeling
- Understand difficulty better

### 📊 Feature Display
All 10 features shown with values:
- Max Stretch
- Max Chord Size
- Note Density
- Left Hand Activity
- Average Tempo
- Dynamic Range
- Poly Voice Count
- Octave Jump Frequency
- Thirds Frequency
- Polyrhythm Score

### ⌨️ Keyboard Shortcuts
- **1-5** - Assign label (1=Far Reach, 2=Double Thirds, etc.)
- **←/→** - Navigate files
- **Space** - Play/pause MIDI
- **S** - Skip file

### 💾 Progress Tracking
- Auto-saves after each label
- Resume from where you left off
- Shows completion percentage
- Tracks labeling progress

### 🎨 Modern UI
- Clean, responsive design
- Color-coded categories
- Progress indicators
- File information display

---

## 🚀 Usage

### Quick Start

```bash
cd tools\labeling\manual
.venv\Scripts\python.exe start_labeling.py
```

**What it does:**
1. Starts Flask server on port 5000
2. Opens browser at `http://localhost:5000`
3. Loads features from `data/processed/features_all.csv`
4. Loads existing labels (if any)
5. Shows first unlabeled file

**Output:**
```
Starting MIDI Labeling Interface...

✓ Features loaded: 10841 files
✓ Labels loaded: 0 files

🌐 Server running at: http://localhost:5000
📂 Labels will be saved to: data/processed/labels/manual.csv

Press Ctrl+C to stop server
```

---

### Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  MIDI Difficulty Labeling                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  File: example.mid                                      │
│  Progress: 0 / 10841 (0.0%)                            │
│                                                         │
│  ┌─────────────────────────────────────────────┐      │
│  │  🎵 MIDI Player                             │      │
│  │  [Play] [Pause] [Stop]                      │      │
│  └─────────────────────────────────────────────┘      │
│                                                         │
│  📊 Features:                                          │
│  • Max Stretch: 28.5 semitones                        │
│  • Max Chord Size: 7 notes                            │
│  • Note Density: 12.3 notes/sec                       │
│  • Left Hand Activity: 0.42                           │
│  • ... (6 more features)                              │
│                                                         │
│  🏷️ Select Category:                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │    1    │ │    2    │ │    3    │ │    4    │    │
│  │   Far   │ │ Double  │ │Advanced │ │Advanced │    │
│  │  Reach  │ │ Thirds  │ │ Chords  │ │Counter. │    │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │
│                                                         │
│  [← Previous]  [Skip]  [Next →]                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### Labeling Workflow

1. **Listen to MIDI** - Click Play to hear the piece
2. **Review features** - Check the 10 feature values
3. **Assign category** - Press 1-4 (or 1-5 for 5-label)
4. **Move to next** - Automatically advances to next file
5. **Repeat** - Continue until done

**Tips:**
- Use keyboard shortcuts for speed
- Listen to at least 30 seconds of each piece
- Check feature values for edge cases
- Take breaks every 50-100 files

---

## ⚙️ Configuration

### Switch Between 4 and 5 Labels

Edit `../config.py`:

```python
# For 4-label system
DEFAULT_CONFIG = "4_labels"

# For 5-label system
DEFAULT_CONFIG = "5_labels"
```

Then restart server:
```bash
# Ctrl+C to stop
.venv\Scripts\python.exe start_labeling.py
```

**Interface will update:**
- 4-label: Shows 4 buttons (1-4)
- 5-label: Shows 5 buttons (1-5)

---

### Review Existing Labels

To review/correct auto-generated labels:

1. **Copy auto-labels to manual:**
   ```bash
   Copy-Item data\processed\labels\auto_4_labels.csv data\processed\labels\manual.csv
   ```

2. **Start labeling interface:**
   ```bash
   cd tools\labeling\manual
   .venv\Scripts\python.exe start_labeling.py
   ```

3. **Review and correct:**
   - Interface loads existing labels
   - Shows labeled files
   - You can relabel any file
   - Progress is saved

---

## 📊 Output Format

Labels saved to: `data/processed/labels/manual.csv`

```csv
midi_filename,difficulty_label,timestamp,confidence,method
example.mid,1,2026-02-04T18:25:30.123456,5,manual
```

**Columns:**
- `midi_filename` - File identifier
- `difficulty_label` - Category (0-3 or 0-4)
- `timestamp` - When labeled (ISO format)
- `confidence` - 5 for manual labels (high confidence)
- `method` - Always `manual`

---

## 💡 Best Practices

### 1. Start with Auto-Labels

**Don't label from scratch!**

```bash
# 1. Generate auto-labels first
$env:PYTHONPATH="."; .venv\Scripts\python.exe tools\labeling\auto\auto_label.py --config 4_labels

# 2. Copy to manual
Copy-Item data\processed\labels\auto_4_labels.csv data\processed\labels\manual.csv

# 3. Review and correct
cd tools\labeling\manual
.venv\Scripts\python.exe start_labeling.py
```

**Benefits:**
- Much faster (review vs create)
- Focus on corrections
- Auto-labels are ~60-70% accurate
- You only fix ~30-40% of files

### 2. Label in Batches

**Don't try to label all 10,841 files!**

**Recommended approach:**
1. Label 200-500 files (2-4 hours)
2. Focus on underrepresented categories
3. Ensure balanced distribution
4. Train model with partial labels

**Why this works:**
- 200-500 high-quality labels > 10k auto-labels
- Balanced dataset trains better
- Less labeling fatigue
- Faster iteration

### 3. Use Keyboard Shortcuts

**10x faster than clicking!**

- Press **1-5** to label (no mouse needed)
- Press **→** to skip (if unsure)
- Press **Space** to play/pause
- Press **S** to skip file

**Workflow:**
1. Listen (Space)
2. Check features (eyes)
3. Label (1-5)
4. Next (automatic)

**Speed:** ~30-60 files/hour with practice

### 4. Focus on Edge Cases

**Prioritize these files:**
- Borderline cases (features close to thresholds)
- Underrepresented categories (Double Thirds, Counterpoint)
- Files with conflicting features
- Pieces you recognize

**Skip:**
- Obvious cases (auto-label is clearly correct)
- Files with missing/corrupted data

### 5. Take Breaks

**Labeling fatigue is real!**

- Label 50-100 files at a time
- Take 10-minute breaks
- Review your earlier labels periodically
- Maintain consistency

---

## 🎓 Labeling Guidelines

### Far Reach (0)
**Key indicators:**
- max_stretch > 25 semitones
- Frequent octave jumps
- Wide hand positions

**Listen for:**
- Large leaps between notes
- Stretchy passages
- Wide arpeggios

### Double Thirds (1)
**Key indicators:**
- thirds_frequency > 0.30
- High note_density
- Technical runs

**Listen for:**
- Fast parallel thirds
- Scalar passages in thirds
- Technical difficulty

### Advanced Chords (2) - 4-label
**Key indicators:**
- max_chord_size > 9 notes
- High note_density
- Dense textures

**Listen for:**
- Large, complex chords
- Dense harmonic structures
- Thick textures

### Multiple Voices (2) - 5-label only
**Key indicators:**
- poly_voice_count > 3.5
- Moderate max_chord_size
- High left_hand_activity

**Listen for:**
- Independent melodic lines
- Polyphonic textures
- Voice leading

### Advanced Counterpoint (3 or 4)
**Key indicators:**
- High poly_voice_count
- High polyrhythm_score
- Balanced hand activity

**Listen for:**
- Complex voice independence
- Polyrhythmic patterns
- Contrapuntal writing

---

## 🐛 Troubleshooting

### Server won't start

**Error:** `Address already in use`

**Solution:** Port 5000 is taken
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use different port
# Edit start_labeling.py: app.run(port=5001)
```

### MIDI won't play

**Cause:** Browser MIDI support

**Solution:**
- Use Chrome or Edge (best MIDI support)
- Check browser console for errors
- Ensure MIDI file is valid

### Progress not saving

**Cause:** Write permissions

**Solution:**
```bash
# Check if directory exists
ls data\processed\labels\

# Create if missing
mkdir data\processed\labels\
```

### Interface shows wrong number of buttons

**Cause:** Config mismatch

**Solution:**
1. Check `../config.py` - `DEFAULT_CONFIG` value
2. Restart server (Ctrl+C, then restart)
3. Clear browser cache (Ctrl+Shift+R)

---

## 📈 Performance Tips

### Speed Up Labeling

1. **Use keyboard shortcuts** (10x faster)
2. **Label in focused sessions** (50-100 files)
3. **Skip obvious cases** (auto-label is correct)
4. **Focus on corrections** (not from scratch)

### Improve Accuracy

1. **Listen to each piece** (don't just look at features)
2. **Check multiple features** (not just one)
3. **Be consistent** (use labeling guide)
4. **Review periodically** (check earlier labels)

### Maintain Motivation

1. **Set small goals** (50 files per session)
2. **Track progress** (celebrate milestones)
3. **Take breaks** (avoid fatigue)
4. **See results** (train model, check accuracy)

---

## 📚 See Also

- **[../README.md](../README.md)** - Labeling system overview
- **[../config.py](../config.py)** - Configuration
- **[../LABELING_GUIDE.md](../LABELING_GUIDE.md)** - Detailed category definitions
- **[../auto/README.md](../auto/README.md)** - Auto-labeling guide

---

## 🎯 Expected Results

**With manual labeling:**
- **Accuracy:** 70-80% (vs 60-70% auto-only)
- **Distribution:** More balanced
- **Quality:** Higher confidence labels
- **Time:** 2-4 hours for 200-500 files

**Recommended workflow:**
1. Auto-label all files (fast baseline)
2. Manually review 200-500 files (quality boost)
3. Train model (best of both worlds)
4. Achieve 70-80% accuracy

---

**Last Updated:** February 4, 2026  
**Status:** ✅ Production Ready  
**Version:** 2.0
