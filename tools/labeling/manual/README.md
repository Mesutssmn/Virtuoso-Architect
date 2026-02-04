# Manual Labeling Tool 🎹

A web-based interface for manually reviewing and labeling MIDI files. This tool connects to the backend to display MIDI features and save expert judgments.

## Features
- **Dynamic UI**: Automatically adjusts buttons for 4-label or 5-label modes.
- **Keyboard Shortcuts**: Use keys `0-4` to label quickly.
- **Playback**: (Placeholder) Area for MIDI playback.
- **Progress Tracking**: Shows percent completion and remaining files.

## How to Run

### Quick Start
```bash
# Starts server with default 5-label configuration
python start_labeling.py
```

### Advanced Usage
To start the server with a specific configuration manually:
```bash
python labeling_server.py --config 4_labels
```
Then open your browser at **http://localhost:5000**.

## Interface Guide

### Labeling
1.  Review the **Features** panel (Stretch, Chord Size, etc.).
2.  Press a number key (**0-4**) or click a button to assign a label.
    - **0**: Far Reach
    - **1**: Double Thirds
    - **2**: Advanced Chords
    - **3**: Advanced Counterpoint
    - **4**: Multiple Voices (5-Label Mode only)
3.  The tool auto-saves and advances to the next file.

### Navigation
- **Left Arrow**: Previous File
- **Right Arrow**: Next File
