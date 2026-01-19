"""
Step 2: Create cryptographic fingerprints from FRB data (FIXED VERSION)
"""

import pandas as pd
import hashlib
import json
from datetime import datetime, timedelta

def mjd_to_utc(mjd):
    """
    Convert Modified Julian Date to UTC datetime string
    
    MJD = JD - 2400000.5
    JD 2400000.5 = November 17, 1858 00:00:00 UTC
    """
    if pd.isna(mjd) or mjd == -9999:
        return None
    
    # MJD epoch
    mjd_epoch = datetime(1858, 11, 17, 0, 0, 0)
    
    # Convert
    utc_datetime = mjd_epoch + timedelta(days=float(mjd))
    
    return utc_datetime.isoformat()

def clean_numeric_value(value):
    """
    Clean numeric values (handle -9999, NaN, etc.)
    """
    if pd.isna(value):
        return None
    if value == -9999 or value == '-9999':
        return None
    
    try:
        return float(value)
    except:
        return None

class FRBFingerprint:
    """
    Convert FRB observations into cryptographic fingerprints
    """
    
    def __init__(self):
        pass
    
    def extract_parameters(self, frb_row):
        """
        Extract parameters from CHIME catalog row
        """
        params = {}
        
        # Name
        params['name'] = str(frb_row['tns_name'])
        
        # Timestamp - use mjd_400 (arrival time at 400 MHz)
        params['timestamp'] = mjd_to_utc(frb_row['mjd_400'])
        
        # DM - use dm_fitb (most precise)
        params['dm'] = clean_numeric_value(frb_row['dm_fitb'])
        
        # Fluence
        params['fluence'] = clean_numeric_value(frb_row['fluence'])
        
        # Width - parse from string or use bc_width
        width_val = frb_row['width_fitb']
        if pd.isna(width_val) or width_val == '-9999':
            params['width'] = clean_numeric_value(frb_row['bc_width'])
        else:
            try:
                params['width'] = float(width_val)
            except:
                params['width'] = clean_numeric_value(frb_row['bc_width'])
        
        # Scattering - parse from string
        scat_val = frb_row['scat_time']
        if pd.isna(scat_val) or scat_val == '-9999':
            params['scattering'] = None
        else:
            try:
                params['scattering'] = float(scat_val)
            except:
                params['scattering'] = None
        
        # Add additional unique parameters to reduce collisions
        params['ra'] = clean_numeric_value(frb_row['ra'])
        params['dec'] = clean_numeric_value(frb_row['dec'])
        params['snr'] = clean_numeric_value(frb_row['snr_fitb'])
        params['peak_freq'] = clean_numeric_value(frb_row['peak_freq'])
        
        return params
    
    def normalize_parameters(self, params):
        """
        Normalize parameters for consistent fingerprinting
        """
        normalized = {}
        
        # Name (exact)
        if params.get('name'):
            normalized['name'] = str(params['name'])
        
        # Timestamp (exact)
        if params.get('timestamp'):
            normalized['timestamp'] = str(params['timestamp'])
        
        # DM - round to 4 decimal places (CHIME precision)
        if params.get('dm') is not None:
            normalized['dm'] = round(float(params['dm']), 4)
        
        # Fluence - round to 1 decimal
        if params.get('fluence') is not None:
            normalized['fluence'] = round(float(params['fluence']), 1)
        
        # Width - round to 6 decimals (microsecond precision)
        if params.get('width') is not None:
            normalized['width_ms'] = round(float(params['width']), 6)
        
        # Scattering - round to 5 decimals
        if params.get('scattering') is not None:
            normalized['scattering_ms'] = round(float(params['scattering']), 5)
        
        # Sky position - round to 2 decimals (arcminute precision)
        if params.get('ra') is not None:
            normalized['ra'] = round(float(params['ra']), 2)
        if params.get('dec') is not None:
            normalized['dec'] = round(float(params['dec']), 2)
        
        # SNR - round to 1 decimal
        if params.get('snr') is not None:
            normalized['snr'] = round(float(params['snr']), 1)
        
        # Peak frequency - round to 1 decimal
        if params.get('peak_freq') is not None:
            normalized['peak_freq'] = round(float(params['peak_freq']), 1)
        
        return normalized
    
    def create_fingerprint(self, params):
        """
        Create SHA-256 fingerprint from parameters
        """
        # Normalize
        norm = self.normalize_parameters(params)
        
        # Convert to canonical JSON (sorted keys)
        canonical = json.dumps(norm, sort_keys=True, ensure_ascii=True)
        
        # Hash
        fingerprint = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
        
        return {
            'fingerprint': fingerprint,
            'normalized_params': norm,
            'canonical_json': canonical
        }
    
    def process_catalog(self, df):
        """
        Process entire catalog and create fingerprints for all FRBs
        """
        print("="*70)
        print("CREATING FRB FINGERPRINTS (ENHANCED VERSION)")
        print("="*70)
        
        results = []
        
        for idx, row in df.iterrows():
            # Extract parameters
            params = self.extract_parameters(row)
            
            # Create fingerprint
            fp_data = self.create_fingerprint(params)
            
            # Store result
            result = {
                'index': idx,
                'frb_name': params.get('name', f'FRB_{idx}'),
                'fingerprint': fp_data['fingerprint'],
                **fp_data['normalized_params']
            }
            
            results.append(result)
            
            # Progress indicator
            if (idx + 1) % 100 == 0:
                print(f"   Processed {idx + 1} FRBs...")
        
        print(f"\n✓ Created fingerprints for {len(results)} FRBs")
        
        return pd.DataFrame(results)

def save_fingerprints(fingerprints_df, output_path):
    """
    Save fingerprints to CSV
    """
    fingerprints_df.to_csv(output_path, index=False)
    print(f"\n✓ Saved fingerprints to: {output_path}")

def demonstrate_uniqueness(fingerprints_df):
    """
    Show that fingerprints are unique
    """
    print("\n" + "="*70)
    print("DEMONSTRATING FINGERPRINT UNIQUENESS")
    print("="*70)
    
    # Check for duplicates
    duplicates = fingerprints_df['fingerprint'].duplicated().sum()
    print(f"\nDuplicate fingerprints: {duplicates}")
    
    if duplicates == 0:
        print("✓ All fingerprints are COMPLETELY UNIQUE!")
    else:
        print(f"⚠ WARNING: Found {duplicates} duplicate fingerprints")
        print("   Analyzing duplicates...")
        
        # Show duplicate examples
        dup_prints = fingerprints_df[fingerprints_df['fingerprint'].duplicated(keep=False)]
        dup_prints_sorted = dup_prints.sort_values('fingerprint')
        
        print(f"\n   First few duplicate groups:")
        for fp in dup_prints_sorted['fingerprint'].unique()[:3]:
            matches = dup_prints[dup_prints['fingerprint'] == fp]
            print(f"\n   Fingerprint: {fp[:32]}...")
            print(f"   FRBs sharing this fingerprint:")
            for _, row in matches.iterrows():
                print(f"      - {row['frb_name']} (DM={row.get('dm', 'N/A')})")
    
    # Show first 5 fingerprints with full details
    print(f"\n" + "="*70)
    print("FIRST 5 FRB FINGERPRINTS (with details):")
    print("="*70)
    for idx, row in fingerprints_df.head().iterrows():
        print(f"\n{row['frb_name']}:")
        print(f"   Timestamp: {row.get('timestamp', 'N/A')}")
        print(f"   DM: {row.get('dm', 'N/A')} pc/cm³")
        print(f"   Fluence: {row.get('fluence', 'N/A')} Jy·ms")
        print(f"   Width: {row.get('width_ms', 'N/A')} ms")
        print(f"   SNR: {row.get('snr', 'N/A')}")
        print(f"   Fingerprint: {row['fingerprint'][:48]}...")

# Main execution
if __name__ == "__main__":
    # Load catalog
    catalog_path = "data/chimefrbcat1.csv"  # Adjust filename
    df = pd.read_csv(catalog_path)
    print(f"✓ Loaded {len(df)} FRBs from catalog\n")
    
    # Create fingerprint generator
    fp_generator = FRBFingerprint()
    
    # Process entire catalog
    fingerprints = fp_generator.process_catalog(df)
    
    # Save results
    output_path = "output/frb_fingerprints_enhanced.csv"
    save_fingerprints(fingerprints, output_path)
    
    # Demonstrate uniqueness
    demonstrate_uniqueness(fingerprints)
    
    print("\n" + "="*70)
    print("✓ ENHANCED FINGERPRINT GENERATION COMPLETE")
    print("="*70)
    print(f"\nYou now have cryptographic fingerprints for {len(fingerprints)} FRBs")
    print(f"Each fingerprint uses 10 parameters for maximum uniqueness")
    print(f"Output saved to: {output_path}")