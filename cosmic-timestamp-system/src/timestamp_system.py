"""
Timestamp system module for API functions
"""
import pandas as pd
import hashlib
import json
from datetime import datetime
import os

# Initialize system singleton
_system = None

def get_system():
    """Get or create the CosmicTimestampSystem instance"""
    global _system
    if _system is None:
        # Use absolute path for Vercel
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', 'output', 'frb_fingerprints_enhanced.csv')
        db_path = os.path.abspath(db_path)
        _system = CosmicTimestampSystem(db_path)
    return _system

class CosmicTimestampSystem:
    """
    Seal documents with FRB fingerprints and verify them
    """
    
    def __init__(self, fingerprints_db_path):
        """
        Load the FRB fingerprints database
        """
        self.fingerprints_db = pd.read_csv(fingerprints_db_path)
    
    def get_available_frbs(self, limit=10):
        """
        Get list of available FRBs for sealing
        """
        # Select columns that exist
        available_cols = ['frb_name', 'fingerprint']
        if 'timestamp' in self.fingerprints_db.columns:
            available_cols.append('timestamp')
        if 'dm' in self.fingerprints_db.columns:
            available_cols.append('dm')
        
        return self.fingerprints_db.head(limit)[available_cols]
    
    def seal_document(self, document_content, frb_name):
        """
        Seal a document with an FRB timestamp
        """
        # Find the FRB
        frb_match = self.fingerprints_db[self.fingerprints_db['frb_name'] == frb_name]
        
        if len(frb_match) == 0:
            return None
        
        frb = frb_match.iloc[0]
        
        # Hash the document
        doc_hash = hashlib.sha256(document_content.encode('utf-8')).hexdigest()
        
        # Create the cosmic seal
        seal = {
            'document_hash': doc_hash,
            'frb_name': frb['frb_name'],
            'frb_fingerprint': frb['fingerprint'],
            'frb_timestamp': str(frb.get('timestamp', 'Unknown')),
            'frb_dm': float(frb.get('dm', 0)) if pd.notna(frb.get('dm')) else None,
            'frb_ra': float(frb.get('ra', 0)) if pd.notna(frb.get('ra')) else None,
            'frb_dec': float(frb.get('dec', 0)) if pd.notna(frb.get('dec')) else None,
            'sealed_at_utc': datetime.utcnow().isoformat(),
            'seal_version': '1.0'
        }
        
        # Sign the seal
        seal_data = json.dumps(seal, sort_keys=True)
        seal_signature = hashlib.sha256(seal_data.encode('utf-8')).hexdigest()
        seal['signature'] = seal_signature
        
        return seal
    
    def verify_seal(self, document_content, seal):
        """
        Verify that a cosmic seal is valid
        Returns: (is_valid: bool, message: str)
        """
        # Verify seal structure
        required_fields = ['document_hash', 'frb_name', 'frb_fingerprint', 'signature']
        for field in required_fields:
            if field not in seal:
                return False, f"Missing required field: {field}"
        
        # Verify signature
        seal_copy = seal.copy()
        provided_signature = seal_copy.pop('signature')
        
        seal_data = json.dumps(seal_copy, sort_keys=True)
        expected_signature = hashlib.sha256(seal_data.encode('utf-8')).hexdigest()
        
        if provided_signature != expected_signature:
            return False, "Seal signature invalid - seal has been tampered with"
        
        # Verify FRB exists in database
        frb_match = self.fingerprints_db[
            self.fingerprints_db['frb_name'] == seal['frb_name']
        ]
        
        if len(frb_match) == 0:
            return False, f"FRB '{seal['frb_name']}' not found in public catalog"
        
        frb = frb_match.iloc[0]
        
        # Verify FRB fingerprint matches
        if frb['fingerprint'] != seal['frb_fingerprint']:
            return False, "FRB fingerprint mismatch - seal references incorrect FRB data"
        
        # Verify document hash
        doc_hash = hashlib.sha256(document_content.encode('utf-8')).hexdigest()
        if doc_hash != seal['document_hash']:
            return False, "Document has been modified since sealing"
        
        # All checks passed
        frb_time = seal.get('frb_timestamp', 'Unknown')
        frb_dm = seal.get('frb_dm', 'Unknown')
        return True, f"✓ Valid cosmic timestamp from FRB at {frb_time} (DM={frb_dm} pc/cm³)"

# Convenience functions for API
def load_frbs(limit=50):
    """Load FRBs for API"""
    system = get_system()
    frbs = []
    available = system.get_available_frbs(limit)
    
    for _, row in available.iterrows():
        frbs.append({
            'name': row['frb_name'],
            'timestamp': str(row.get('timestamp', 'Unknown')),
            'dm': round(float(row.get('dm', 0)), 2) if pd.notna(row.get('dm')) else None,
            'distance_estimate': f"{round(float(row.get('dm', 0)) / 300, 1)} billion light-years" if pd.notna(row.get('dm')) else "Unknown",
            'fingerprint': row['fingerprint'][:16] + '...'
        })
    return frbs

def seal_document(text, frb_name):
    """Seal a document"""
    system = get_system()
    return system.seal_document(text, frb_name)

def verify_seal(text, seal_json):
    """Verify a seal"""
    try:
        seal = json.loads(seal_json) if isinstance(seal_json, str) else seal_json
    except:
        return {'valid': False, 'message': 'Invalid JSON format'}
    
    system = get_system()
    is_valid, message = system.verify_seal(text, seal)
    
    if is_valid:
        return {
            'valid': True,
            'message': message,
            'frb_details': {
                'name': seal['frb_name'],
                'timestamp': seal.get('frb_timestamp', 'Unknown'),
                'dm': seal.get('frb_dm'),
                'distance': f"~{round(float(seal.get('frb_dm', 0)) / 300, 1)} billion light-years away" if seal.get('frb_dm') else "Unknown"
            }
        }
    else:
        return {'valid': False, 'message': message}

