"""
Data Manager for Giant MIDI Dataset
Processes raw MIDI metadata and generates cleaned CSV file.
"""

import pandas as pd
import os
from pathlib import Path


def extract_composer(filename):
    """
    Extract composer name from MIDI filename.
    
    Logic: Filename format is typically: Surname-FirstName-Title-ID.mid
    
    Args:
        filename (str): MIDI filename
        
    Returns:
        str: Composer name in "Surname FirstName" format
    """
    clean_name = str(filename).replace(".mid", "")
    parts = clean_name.split('-')
    
    # Logic: Surname is usually first, First name second
    if len(parts) >= 3:
        return f"{parts[0]} {parts[1]}".title()
    elif len(parts) == 2:
        return parts[0].title()
    else:
        return "Unknown"


def extract_title(row):
    """
    Extract piece title from MIDI filename.
    
    Args:
        row (pd.Series): DataFrame row with 'midi_filename' column
        
    Returns:
        str: Piece title
    """
    filename = str(row['midi_filename']).replace(".mid", "")
    parts = filename.split('-')
    
    # If we grabbed 2 words for composer, the rest is the title (minus the ID at the end)
    if len(parts) > 3:
        title_parts = parts[2:-1]
        return " ".join(title_parts).title()
    else:
        return row.get('canonical_title', 'Unknown')


def process_giant_midi(input_csv_path, output_csv_path):
    """
    Process Giant MIDI raw CSV and generate cleaned metadata file.
    
    Args:
        input_csv_path (str): Path to raw CSV file
        output_csv_path (str): Path to save cleaned CSV file
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    print(f"Loading raw data from: {input_csv_path}")
    
    # Check if input file exists
    if not os.path.exists(input_csv_path):
        raise FileNotFoundError(f"Input CSV not found: {input_csv_path}")
    
    # Load the raw data
    df = pd.read_csv(input_csv_path)
    print(f"Loaded {len(df)} records")
    
    # Extract composer names
    print("Extracting composer names...")
    df['canonical_composer'] = df['midi_filename'].apply(extract_composer)
    
    # Extract titles
    print("Extracting piece titles...")
    df['canonical_title'] = df.apply(extract_title, axis=1)
    
    # Save the new clean registry
    print(f"Saving cleaned data to: {output_csv_path}")
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    
    print(f"✓ Successfully processed {len(df)} records")
    print(f"✓ Unique composers: {df['canonical_composer'].nunique()}")
    print(f"✓ Sample composers: {df['canonical_composer'].value_counts().head(5).to_dict()}")
    
    return df


if __name__ == "__main__":
    # Default paths
    project_root = Path(__file__).parent.parent
    input_path = project_root / "data" / "raw" / "giant_midi_reconstructed.csv"
    output_path = project_root / "data" / "processed" / "giant_midi_fixed.csv"
    
    # Process the data
    df = process_giant_midi(str(input_path), str(output_path))
    
    print("\n" + "="*50)
    print("Data processing complete!")
    print("="*50)
