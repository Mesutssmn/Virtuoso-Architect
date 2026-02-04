# Manual MIDI Difficulty Labeling

Web-based interface for manually labeling MIDI files.

## 🎯 Features

- **Web Interface**: Modern, responsive UI
- **MIDI Playback**: Listen while labeling
- **Feature Visualization**: See all 10 features
- **Keyboard Shortcuts**: Fast labeling (1-5 keys)
- **Progress Tracking**: Auto-save and resume
- **Flexible**: Works with any label configuration

## 🚀 Quick Start

```bash
cd tools\labeling\manual
.venv\Scripts\python.exe start_labeling.py
```

Opens browser at `http://localhost:5000`

## ⌨️ Keyboard Shortcuts

- **1-5**: Assign label
- **←/→**: Navigate files
- **Space**: Play/pause MIDI
- **S**: Skip file

## 📊 Interface

### File Info
- Filename
- Current progress (X/Y)
- Completion percentage

### Features Display
All 10 features with values:
- Max Stretch
- Thirds Frequency
- Max Chord Size
- Note Density
- Left Hand Activity
- Poly Voice Count
- Octave Jump Frequency
- Polyrhythm Score
- Avg Tempo
- Dynamic Range

### Labeling Buttons
Color-coded buttons for each category

## 💾 Data Storage

Labels saved to: `data/processed/labels/manual.csv`

Progress tracked in: `data/processed/labels/labeling_progress.json`

## 🔧 Configuration

The interface automatically adapts to the label configuration in `../config.py`.

To change label count:
1. Edit `config.py`
2. Set `DEFAULT_CONFIG = "4_labels"` or `"5_labels"`
3. Restart server

## 💡 Best Practices

1. **Listen to the MIDI** - Don't rely only on features
2. **Use keyboard shortcuts** - Much faster
3. **Take breaks** - Labeling fatigue is real
4. **Be consistent** - Use the guide
5. **Review periodically** - Check your earlier labels

## 📖 Labeling Guide

See [../LABELING_GUIDE.md](../LABELING_GUIDE.md) for:
- Category definitions
- Decision flowchart
- Examples
- Edge cases

## 🐛 Troubleshooting

**Server won't start:**
- Check if port 5000 is available
- Install dependencies: `pip install flask flask-cors`

**MIDI won't play:**
- Check browser MIDI support
- Try different browser (Chrome recommended)

**Progress not saving:**
- Check write permissions
- Verify `data/processed/labels/` exists

## 🎓 Tips

- **Start with extremes** - Label obvious cases first
- **Use auto-labels** - Review/correct instead of from scratch
- **Batch similar files** - More consistent
- **Note patterns** - Document your decision process
