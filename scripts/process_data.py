"""
Data Processing Script
Processes Giant MIDI raw CSV and generates cleaned metadata file.
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from data_manager import process_giant_midi


def main():
    """
    Main function to process Giant MIDI dataset.
    """
    # Define paths
    input_path = project_root / "data" / "raw" / "giant_midi_reconstructed.csv"
    output_path = project_root / "data" / "processed" / "giant_midi_fixed.csv"
    
    print("="*60)
    print("Giant MIDI Dataset Processing")
    print("="*60)
    print(f"\nInput: {input_path}")
    print(f"Output: {output_path}\n")
    
    # Check if input exists
    if not input_path.exists():
        print(f"❌ Error: Input file not found!")
        print(f"   Expected: {input_path}")
        print(f"\n   Please ensure 'giant_midi_reconstructed.csv' exists in data/raw/")
        return
    
    # Process data
    try:
        df = process_giant_midi(str(input_path), str(output_path))
        
        print("\n" + "="*60)
        print("✓ Data processing completed successfully!")
        print("="*60)
        print(f"\nProcessed {len(df)} MIDI files")
        print(f"Output saved to: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
