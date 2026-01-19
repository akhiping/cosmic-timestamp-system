"""
Step 1: Explore the CHIME FRB Catalog
"""

import pandas as pd
import numpy as np

def load_catalog(filepath):
    """Load the CHIME catalog CSV"""
    print("="*70)
    print("LOADING CHIME FRB CATALOG")
    print("="*70)
    
    df = pd.read_csv(filepath)
    
    print(f"\n✓ Loaded {len(df)} FRB detections")
    print(f"\n✓ Available columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    
    return df

def analyze_catalog(df):
    """Analyze the catalog structure and contents"""
    print("\n" + "="*70)
    print("CATALOG ANALYSIS")
    print("="*70)
    
    # Basic info
    print(f"\nTotal FRBs: {len(df)}")
    print(f"\nData types:")
    print(df.dtypes)
    
    # Check for missing values
    print(f"\nMissing values per column:")
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            print(f"   {col}: {count} ({count/len(df)*100:.1f}%)")
    
    # Show first few rows
    print("\n" + "="*70)
    print("FIRST 5 FRBs:")
    print("="*70)
    print(df.head())
    
    # Show summary statistics
    print("\n" + "="*70)
    print("NUMERICAL SUMMARY:")
    print("="*70)
    print(df.describe())
    
    return df

def identify_key_columns(df):
    """
    Identify which columns we'll use for fingerprints
    """
    print("\n" + "="*70)
    print("IDENTIFYING KEY COLUMNS FOR FINGERPRINTS")
    print("="*70)
    
    # Common CHIME column names (may vary)
    possible_columns = {
        'name': ['tns_name', 'name', 'frb_name', 'source_name'],
        'timestamp': ['utc', 'mjd', 'datetime', 'arrival_time', 'time'],
        'dm': ['dm', 'dispersion_measure', 'DM'],
        'fluence': ['fluence', 'flux', 'peak_flux'],
        'width': ['width', 'width_ms', 'duration', 'pulse_width'],
        'scattering': ['scattering', 'scattering_time', 'scatter']
    }
    
    found_columns = {}
    
    for key, possible_names in possible_columns.items():
        for col in df.columns:
            if col.lower() in [p.lower() for p in possible_names]:
                found_columns[key] = col
                print(f"✓ Found {key:12} → using column '{col}'")
                break
        
        if key not in found_columns:
            print(f"✗ Missing {key:12} → will skip or need manual mapping")
    
    return found_columns

def show_sample_frb(df, column_mapping):
    """
    Display a complete FRB record
    """
    print("\n" + "="*70)
    print("EXAMPLE FRB (First Detection):")
    print("="*70)
    
    frb = df.iloc[0]
    
    print(f"\nRaw data:")
    print(frb)
    
    print(f"\nExtracted parameters:")
    for key, col_name in column_mapping.items():
        if col_name in df.columns:
            value = frb[col_name]
            print(f"   {key:15} = {value}")

# Main execution
if __name__ == "__main__":
    # CHANGE THIS to match your actual file path
    catalog_path = "data/chimefrbcat1.csv"
    
    # Load
    df = load_catalog(catalog_path)
    
    # Analyze
    df = analyze_catalog(df)
    
    # Identify columns
    columns = identify_key_columns(df)
    
    # Show example
    show_sample_frb(df, columns)
    
    print("\n" + "="*70)
    print("✓ DATA EXPLORATION COMPLETE")
    print("="*70)
    print(f"\nNext step: Create FRB fingerprints using these {len(columns)} parameters")