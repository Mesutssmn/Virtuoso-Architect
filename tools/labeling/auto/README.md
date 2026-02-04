# Auto-Labeling Tool 🤖

This tool automatically assigns difficulty labels to MIDI files based on pre-extracted features. It uses a rule-based scoring system defined in `config.py`.

## Logic
The labeler calculates a score for each category based on features like:
- Max chord size
- Polyphony count
- Hand stretch (interval size)
- Note density
- Thirds frequency

The category with the highest score wins.

## Usage

### Run with Default Config (5 Labels)
```bash
python auto_label.py
```

### Run with 4 Labels
```bash
python auto_label.py --config 4_labels
```

### Options
- `--config`: Choose `4_labels` or `5_labels`.
- `--features`: Path to input features CSV (Default: `data/processed/features_all.csv`).
- `--output`: Custom output path.
- `--overwrite`: Force overwrite if output file exists.

## Outputs
Files are saved to `data/processed/labels/`:
- `auto_4_labels.csv`
- `auto_5_labels.csv`
