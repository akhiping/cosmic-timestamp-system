import pandas as pd
import numpy as np
from datetime import datetime

# Step 1: Load the CHIME FRB catalog
def load_chime_catalog(file_path):
    """
    Load CHIME FRB catalog from CSV file
    """
    print(f"Loading FRB data from {file_path}...")
    
    # Read the CSV
    df = pd.read_csv(file_path)
    
    print(f"✓ Loaded {len(df)} FRB detections")
    print(f"✓ Columns available: {list(df.columns)}")
    
    return df

# Step 2: Explore the data
def explore_frbs(df):
    """
    Print summary statistics about the FRB catalog
    """
    print("\n" + "="*50)
    print("FRB CATALOG SUMMARY")
    print("="*50)
    
    # Basic stats
    print(f"\nTotal FRBs: {len(df)}")
    print(f"Date range: {df['utc'].min()} to {df['utc'].max()}")
    
    # Dispersion measure stats
    print(f"\nDispersion Measure (DM):")
    print(f"  Min: {df['dm'].min():.1f} pc/cm³")
    print(f"  Max: {df['dm'].max():.1f} pc/cm³")
    print(f"  Mean: {df['dm'].mean():.1f} pc/cm³")
    
    # Repeaters vs non-repeaters
    if 'repeater' in df.columns:
        repeaters = df['repeater'].sum()
        print(f"\nRepeating FRBs: {repeaters}")
        print(f"One-off FRBs: {len(df) - repeaters}")
    
    # Show first few FRBs
    print("\n" + "="*50)
    print("FIRST 5 FRBs:")
    print("="*50)
    print(df.head())

# Step 3: Extract parameters for a specific FRB
def get_frb_parameters(df, frb_name):
    """
    Get all parameters for a specific FRB
    """
    frb = df[df['tns_name'] == frb_name]
    
    if len(frb) == 0:
        print(f"FRB {frb_name} not found!")
        return None
    
    frb = frb.iloc[0]  # Get first (only) row
    
    params = {
        'name': frb['tns_name'],
        'timestamp': frb['utc'],
        'dm': frb['dm'],
        'fluence': frb['fluence'] if 'fluence' in frb else None,
        'width': frb['width'] if 'width' in frb else None,
        'scattering': frb['scattering'] if 'scattering' in frb else None,
    }
    
    return params

# Main execution
if __name__ == "__main__":
    # REPLACE THIS with the actual path to your downloaded CSV
    catalog_file = "chime_frb_catalog.csv"
    
    # Load the data
    frb_df = load_chime_catalog(catalog_file)
    
    # Explore it
    explore_frbs(frb_df)
    
    # Get parameters for a specific FRB
    print("\n" + "="*50)
    print("EXTRACTING SPECIFIC FRB:")
    print("="*50)
    example_frb = frb_df['tns_name'].iloc[0]  # Get first FRB name
    params = get_frb_parameters(frb_df, example_frb)
    
    if params:
        print(f"\nParameters for {params['name']}:")
        for key, value in params.items():
            print(f"  {key}: {value}")