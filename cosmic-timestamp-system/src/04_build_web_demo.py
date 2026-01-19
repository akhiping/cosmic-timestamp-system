"""
Step 4: Web interface for Cosmic Timestamp System
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import hashlib
import json
from datetime import datetime
import os

class CosmicTimestampAPI:
    def __init__(self, fingerprints_path):
        self.db = pd.read_csv(fingerprints_path)
        print(f"✓ Loaded {len(self.db)} FRB fingerprints")
    
    def get_recent_frbs(self, limit=20):
        """Get recent FRBs for display"""
        frbs = []
        for _, row in self.db.head(limit).iterrows():
            frbs.append({
                'name': row['frb_name'],
                'timestamp': row['timestamp'],
                'dm': round(row['dm'], 2),
                'distance_estimate': f"{round(row['dm'] / 300, 1)} billion light-years",
                'fingerprint': row['fingerprint'][:16] + '...'
            })
        return frbs
    
    def seal_document(self, text, frb_name):
        """Seal a document"""
        frb_match = self.db[self.db['frb_name'] == frb_name]
        
        if len(frb_match) == 0:
            return None
        
        frb = frb_match.iloc[0]
        doc_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        
        seal = {
            'document_hash': doc_hash,
            'document_preview': text[:200] + '...' if len(text) > 200 else text,
            'frb_name': frb['frb_name'],
            'frb_fingerprint': frb['fingerprint'],
            'frb_timestamp': str(frb['timestamp']),
            'frb_dm': float(frb['dm']),
            'sealed_at_utc': datetime.utcnow().isoformat(),
            'seal_version': '1.0'
        }
        
        seal_data = json.dumps({k: v for k, v in seal.items() if k != 'document_preview'}, sort_keys=True)
        seal['signature'] = hashlib.sha256(seal_data.encode('utf-8')).hexdigest()
        
        return seal
    
    def verify_seal(self, text, seal_json):
        """Verify a seal"""
        try:
            seal = json.loads(seal_json)
        except:
            return {'valid': False, 'message': 'Invalid JSON format'}
        
        # Check signature
        seal_copy = {k: v for k, v in seal.items() if k not in ['signature', 'document_preview']}
        seal_data = json.dumps(seal_copy, sort_keys=True)
        expected_sig = hashlib.sha256(seal_data.encode('utf-8')).hexdigest()
        
        if seal.get('signature') != expected_sig:
            return {'valid': False, 'message': 'Seal has been tampered with'}
        
        # Check FRB exists
        frb_match = self.db[self.db['frb_name'] == seal['frb_name']]
        if len(frb_match) == 0:
            return {'valid': False, 'message': 'FRB not found in public catalog'}
        
        frb = frb_match.iloc[0]
        if frb['fingerprint'] != seal['frb_fingerprint']:
            return {'valid': False, 'message': 'FRB fingerprint mismatch'}
        
        # Check document
        doc_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        if doc_hash != seal['document_hash']:
            return {'valid': False, 'message': 'Document has been modified'}
        
        return {
            'valid': True,
            'message': f"✓ Valid cosmic timestamp from FRB detected at {seal['frb_timestamp']}",
            'frb_details': {
                'name': seal['frb_name'],
                'timestamp': seal['frb_timestamp'],
                'dm': seal['frb_dm'],
                'distance': f"~{round(seal['frb_dm'] / 300, 1)} billion light-years away"
            }
        }

# Initialize Flask app
# Set template folder to root-level templates directory
import os
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

# Get absolute path to CSV file for production
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'frb_fingerprints_enhanced.csv'))
api = CosmicTimestampAPI(csv_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/frbs')
def get_frbs():
    """API endpoint to get available FRBs"""
    frbs = api.get_recent_frbs(50)
    return jsonify(frbs)

@app.route('/api/seal', methods=['POST'])
def seal():
    """API endpoint to seal a document"""
    data = request.json
    text = data.get('text', '')
    frb_name = data.get('frb_name', '')
    
    if not text or not frb_name:
        return jsonify({'error': 'Missing text or FRB name'}), 400
    
    seal = api.seal_document(text, frb_name)
    
    if seal is None:
        return jsonify({'error': 'FRB not found'}), 404
    
    return jsonify(seal)

@app.route('/api/verify', methods=['POST'])
def verify():
    """API endpoint to verify a seal"""
    data = request.json
    text = data.get('text', '')
    seal_json = data.get('seal', '')
    
    if not text or not seal_json:
        return jsonify({'error': 'Missing text or seal'}), 400
    
    result = api.verify_seal(text, seal_json)
    return jsonify(result)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌌 COSMIC TIMESTAMP SYSTEM - WEB INTERFACE")
    print("="*70)
    print("\n✓ Server starting...")
    
    # Production configuration (Render, Heroku, etc.)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    if debug:
        print("✓ Open your browser to: http://localhost:5000")
    else:
        print(f"✓ Server running on port {port}")
    
    print("\n")
    app.run(host='0.0.0.0', port=port, debug=debug)