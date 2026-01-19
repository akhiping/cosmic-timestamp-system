# 🌌 Cosmic Timestamp System

**Unforgeable Timestamps Verified by Fast Radio Bursts from Across the Universe**

![Cosmic Timestamp System](/home/akhiping/Documents/Mantaray/cosmic-timestamp-system/screenshots/cosmic-timestamp-hero.png)

## What is this?

A novel cryptographic timestamp system that uses **Fast Radio Bursts (FRBs)** - mysterious cosmic explosions from billions of light-years away - as unforgeable temporal anchors for documents and data.

Instead of trusting a central authority for timestamps, this system leverages cosmic events that:
- Are detected globally by multiple independent observatories
- Cannot be predicted or manipulated
- Are permanently recorded in public astronomical catalogs
- Originate from across the universe

**Result:** Provably unforgeable timestamps verified by the cosmos itself.

---

## 🚀 Live Demo

**[Try it here](#)** https://cosmic-timestamp-system.onrender.com


Or run locally:
```bash
git clone https://github.com/yourusername/cosmic-timestamp-system
cd cosmic-timestamp-system
pip install -r requirements.txt
python src/04_build_web_demo.py
# Open http://localhost:5000
```

---

## How It Works

### 1. **FRB Detection**
Fast Radio Bursts are millisecond-duration radio pulses detected by telescopes like CHIME (Canadian Hydrogen Intensity Mapping Experiment). Each FRB has unique parameters:
- **Timestamp**: Exact arrival time (microsecond precision)
- **Dispersion Measure (DM)**: Shows how far it traveled through space
- **Spectral Properties**: Frequency distribution, peak flux, pulse width
- **Sky Position**: Where in the sky it came from

### 2. **Cryptographic Fingerprinting**
Each FRB detection is converted into a unique cryptographic fingerprint using SHA-256 hashing of its normalized parameters:
```python
FRB Parameters → Normalization → SHA-256 Hash → Unique Fingerprint
```

**Example:**
- FRB20180725A detected at `2018-07-25T17:59:42.996990`
- DM: `715.8093 pc/cm³` (~2.4 billion light-years away)
- Fingerprint: `6b8b15267ec67ecfcc6fcfeaa9e8b8c8...`

### 3. **Document Sealing**
To timestamp a document:
1. User selects an FRB from the public catalog
2. Document hash is computed (SHA-256)
3. A "cosmic seal" is created combining:
   - Document hash
   - FRB fingerprint
   - FRB timestamp and parameters
   - Current sealing time
4. The seal itself is cryptographically signed

**Key Insight:** The document is provably created AFTER the FRB occurred, since you cannot seal with an FRB that hasn't happened yet.

### 4. **Verification**
Anyone can verify a seal by:
1. Recomputing the document hash
2. Looking up the FRB in the public CHIME catalog
3. Verifying the FRB fingerprint matches catalog data
4. Checking the seal's cryptographic signature

**No central authority needed** - verification uses public astronomical data.

---

## Why This Matters

### **Current Timestamp Problems:**
- Centralized authorities can be corrupted or coerced
- System clocks can be manipulated
- Traditional digital signatures depend on PKI trust chains
- Blockchain timestamps still rely on network consensus

### **Cosmic Timestamps Solve This:**
- ✅ **Unforgeable**: FRBs originate billions of light-years away
- ✅ **Decentralized**: Multiple observatories detect the same events
- ✅ **Publicly Verifiable**: Astronomical catalogs are open to all
- ✅ **Permanent**: FRB detections are archived indefinitely
- ✅ **Independent**: No reliance on Earth-based infrastructure

---

## Use Cases

### 1. **Scientific Priority Claims**
Researchers can prove when they made a discovery by sealing their findings with an FRB timestamp.

### 2. **AI Model Provenance**
Prove when an AI model was trained, preventing data leakage and backdating claims.

### 3. **Legal Documents**
Create timestamps for contracts, patents, or evidence that can't be disputed.

### 4. **Blockchain Applications**
Use FRBs as a source of verifiable randomness or as anchors for cross-chain verification.

### 5. **Digital Art / NFTs**
Timestamp creative works with cosmic events for provenance.

---

## Technical Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     COSMIC TIMESTAMP SYSTEM                  │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  CHIME FRB   │─────▶│  Fingerprint │─────▶│   Sealing    │
│   Catalog    │      │  Generator   │      │    Engine    │
│  (600 FRBs)  │      │  (SHA-256)   │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
                                                    │
                                                    ▼
                                           ┌──────────────┐
                                           │ Verification │
                                           │    Engine    │
                                           └──────────────┘
                                                    │
                                                    ▼
                                           ┌──────────────┐
                                           │  Web UI /    │
                                           │     API      │
                                           └──────────────┘
```

### **Components:**

**1. Data Pipeline (`src/01_explore_data.py`)**
- Loads CHIME FRB Catalog (600 detections)
- Parses parameters: timestamp (MJD→UTC), DM, fluence, width, SNR, sky position

**2. Fingerprint Generator (`src/02_create_fingerprints.py`)**
- Normalizes FRB parameters to account for measurement precision
- Creates deterministic SHA-256 hashes
- Ensures 100% uniqueness (0 collisions across 600 FRBs)

**3. Timestamp System (`src/03_timestamp_system.py`)**
- Seals documents with FRB fingerprints
- Generates cryptographic seals with signatures
- Verifies seals against public catalog

**4. Web Interface (`src/04_build_web_demo.py`)**
- Flask-based API and UI
- Real-time FRB selection
- Interactive seal creation and verification

---

## Installation & Setup

### **Prerequisites:**
- Python 3.8+
- pip

### **Quick Start:**
```bash
# Clone the repository
git clone https://github.com/yourusername/cosmic-timestamp-system.git
cd cosmic-timestamp-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the web interface
python src/04_build_web_demo.py

# Open http://localhost:5000 in your browser
```

### **Project Structure:**
```
cosmic-timestamp-system/
├── data/
│   └── FRBs_20181030_public.csv      # CHIME FRB Catalog
├── src/
│   ├── 01_explore_data.py             # Data exploration
│   ├── 02_create_fingerprints.py      # Fingerprint generation
│   ├── 03_timestamp_system.py         # Sealing/verification
│   └── 04_build_web_demo.py           # Web interface
├── output/
│   ├── frb_fingerprints_enhanced.csv  # Generated fingerprints
│   └── example_sealed_document_*      # Example seals
├── templates/
│   └── index.html                     # Web UI
├── requirements.txt
└── README.md
```

---

## API Reference

### **GET /api/frbs**
Returns list of available FRBs for sealing.

**Response:**
```json
[
  {
    "name": "FRB20180725A",
    "timestamp": "2018-07-25T17:59:42.996990",
    "dm": 715.81,
    "distance_estimate": "2.4 billion light-years",
    "fingerprint": "6b8b15267ec67ecf..."
  }
]
```

### **POST /api/seal**
Seal a document with an FRB timestamp.

**Request:**
```json
{
  "text": "Your document content here",
  "frb_name": "FRB20180725A"
}
```

**Response:**
```json
{
  "document_hash": "c7959a1e0a501df0...",
  "frb_name": "FRB20180725A",
  "frb_fingerprint": "6b8b15267ec67ecf...",
  "frb_timestamp": "2018-07-25T17:59:42.996990",
  "frb_dm": 715.8093,
  "sealed_at_utc": "2026-01-19T06:42:23.032119",
  "signature": "3febadc2a86c431a..."
}
```

### **POST /api/verify**
Verify a cosmic seal.

**Request:**
```json
{
  "text": "Original document content",
  "seal": "{...seal JSON...}"
}
```

**Response:**
```json
{
  "valid": true,
  "message": "✓ Valid cosmic timestamp from FRB at 2018-07-25T17:59:42.996990",
  "frb_details": {
    "name": "FRB20180725A",
    "timestamp": "2018-07-25T17:59:42.996990",
    "dm": 715.8093,
    "distance": "~2.4 billion light-years away"
  }
}
```

---

## Data Source

This system uses the **CHIME/FRB Public Catalog** (Catalog 1), published by the CHIME/FRB Collaboration:

- **Paper:** [The First CHIME/FRB Fast Radio Burst Catalog](https://arxiv.org/abs/2106.04352)
- **Data:** 600 FRB detections from July 2018 - July 2019
- **License:** Public astronomical data
- **Updates:** CHIME continues to detect FRBs; newer catalogs can be integrated

---

## Limitations & Future Work

### **Current Limitations:**
1. **FRB Rate:** ~3 FRBs detected per day globally → limits real-time timestamping
2. **Latency:** Catalog updates lag detection by weeks/months
3. **Precision:** Limited by measurement accuracy of astronomical instruments
4. **Single Catalog:** Currently uses only CHIME data

### **Future Enhancements:**
- [ ] Real-time integration with FRB alert systems
- [ ] Multi-observatory verification (CHIME + ASKAP + FAST)
- [ ] Smart contract integration for blockchain applications
- [ ] Batch sealing for high-throughput use cases
- [ ] Mobile app for on-the-go timestamping
- [ ] Integration with decentralized storage (IPFS)

---

## Security Considerations

### **Threat Model:**

**What this protects against:**
- ✅ Timestamp forgery (cannot backdate seals)
- ✅ Document tampering (cryptographic hashing)
- ✅ Authority corruption (decentralized verification)
- ✅ Man-in-the-middle attacks (public catalog verification)

**What this doesn't protect against:**
- ❌ Physical theft of unsealed documents
- ❌ Social engineering (convincing someone to seal a backdated claim)
- ❌ Quantum computing attacks on SHA-256 (future concern)

### **Best Practices:**
1. Store seals separately from documents
2. Verify seals using multiple independent catalog sources
3. Use the most recent FRB available to minimize latency
4. Archive seals in multiple locations

---

## Contributing

Contributions welcome! Areas of interest:
- Real-time FRB integration
- Additional observatory support
- Improved UI/UX
- Security audits
- Documentation

**To contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - see LICENSE file for details

---

## Citation

If you use this system in research, please cite:
```bibtex
@software{cosmic_timestamp_2026,
  author = {Akhil Pingali},
  title = {Cosmic Timestamp System: FRB-Verified Unforgeable Timestamps},
  year = {2026},
  url = {https://github.com/yourusername/cosmic-timestamp-system}
}
```

And the CHIME/FRB Catalog:
```bibtex
@article{chime_frb_catalog_2021,
  title={The First CHIME/FRB Fast Radio Burst Catalog},
  author={CHIME/FRB Collaboration and Amiri, Mandana and Andersen, Bridget C. and others},
  journal={The Astrophysical Journal Supplement Series},
  volume={257},
  number={2},
  pages={59},
  year={2021}
}
```

---

## Acknowledgments

- **CHIME/FRB Collaboration** for making FRB data publicly available
- **Anthropic** for Claude AI assistance in development
- The broader **Fast Radio Burst research community**

---


**"Timestamps verified by the universe itself."** 🌌

---

*Built with curiosity, cryptography, and cosmic explosions.*
