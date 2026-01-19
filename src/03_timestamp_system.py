"""
Step 3: Build the cosmic timestamp sealing and verification system (FIXED)
"""

import pandas as pd
import hashlib
import json
from datetime import datetime

class CosmicTimestampSystem:
    """
    Seal documents with FRB fingerprints and verify them
    """
    
    def __init__(self, fingerprints_db_path):
        """
        Load the FRB fingerprints database
        """
        self.fingerprints_db = pd.read_csv(fingerprints_db_path)
        print(f"✓ Loaded {len(self.fingerprints_db)} FRB fingerprints")
    
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
            print(f"✗ FRB '{frb_name}' not found in database")
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
    
    def seal_and_save(self, document_content, frb_name, output_path):
        """
        Seal a document and save both document and seal
        """
        seal = self.seal_document(document_content, frb_name)
        
        if seal is None:
            return False
        
        # Save document
        doc_path = f"{output_path}_document.txt"
        with open(doc_path, 'w') as f:
            f.write(document_content)
        
        # Save seal
        seal_path = f"{output_path}_seal.json"
        with open(seal_path, 'w') as f:
            json.dump(seal, f, indent=2)
        
        print(f"\n✓ Document sealed successfully!")
        print(f"   Document: {doc_path}")
        print(f"   Seal: {seal_path}")
        print(f"   FRB used: {seal['frb_name']}")
        print(f"   FRB timestamp: {seal['frb_timestamp']}")
        print(f"   FRB DM: {seal['frb_dm']} pc/cm³")
        
        return True

def demonstrate_system():
    """
    Demonstrate the cosmic timestamp system
    """
    print("="*70)
    print("COSMIC TIMESTAMP SYSTEM DEMONSTRATION")
    print("="*70)
    
    # Initialize system
    system = CosmicTimestampSystem("output/frb_fingerprints_enhanced.csv")
    
    # Show available FRBs
    print("\nAvailable FRBs for sealing:")
    print("-"*70)
    available = system.get_available_frbs(5)
    print(available)
    
    # Create a test document
    document = """
RESEARCH BREAKTHROUGH - CONFIDENTIAL

Date: January 19, 2026
Author: Akhil Pingali
Project: FRB-Verified Cosmic Timestamps

DISCOVERY:
I have successfully developed a system that uses Fast Radio Bursts
as cryptographic timestamps. This document serves as proof-of-concept
and establishes priority for this invention.

KEY INNOVATION:
By extracting unique signatures from FRB detections and combining them
with cryptographic hashing, we create unforgeable temporal anchors
that are verified by cosmic events billions of light-years away.

This seal proves this document existed after the FRB event used to sign it.
No Earth-based authority can forge or manipulate this timestamp.

COSMIC NOTARY - Timestamps Verified by the Universe™
    """
    
    # Seal it with first available FRB
    first_frb = available.iloc[0]['frb_name']
    
    print(f"\n\nSealing document with FRB: {first_frb}")
    print("-"*70)
    
    seal = system.seal_document(document, first_frb)
    
    if seal:
        print("\n✓ SEAL CREATED:")
        print(json.dumps(seal, indent=2))
        
        # Verify it
        print("\n\nVerifying seal...")
        print("-"*70)
        is_valid, message = system.verify_seal(document, seal)
        print(message)
        
        # Try tampering with document
        print("\n\nAttempting to verify MODIFIED document...")
        print("-"*70)
        tampered_doc = document + "\n[UNAUTHORIZED TEXT ADDED]"
        is_valid, message = system.verify_seal(tampered_doc, seal)
        print(message)
        
        # Save example
        system.seal_and_save(
            document,
            first_frb,
            "output/breakthrough_sealed_document"
        )

if __name__ == "__main__":
    demonstrate_system()
    
    print("\n" + "="*70)
    print("✓ SYSTEM DEMONSTRATION COMPLETE")
    print("="*70)