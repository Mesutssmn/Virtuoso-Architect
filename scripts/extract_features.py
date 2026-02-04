import sys
from pathlib import Path
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.ml_engine.feature_extract import extract_features_batch

def main():
    parser = argparse.ArgumentParser(description="Extract features from MIDI files")
    parser.add_argument("--input", type=str, default="data/raw_midi", help="Input directory containing MIDI files")
    parser.add_argument("--output", type=str, default="data/processed/features_all.csv", help="Output CSV file")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")

    args = parser.parse_args()

    input_dir = Path(args.input)
    output_file = args.output

    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    print(f"Starting feature extraction from {input_dir}...")
    extract_features_batch(
        midi_files=list(input_dir.glob("*.mid")) + list(input_dir.glob("*.midi")),
        output_csv=output_file,
        n_jobs=args.workers
    )
    print(f"Extraction complete. Features saved to {output_file}")

if __name__ == "__main__":
    main()
