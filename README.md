# SolarSight AI: Intelligent Rooftop Solar Verification

![SolarSight AI Banner](assets/banner.png)

## 🌟 Overview
**SolarSight AI** is a state-of-the-art automated verification pipeline designed to validate rooftop solar photovoltaic (PV) installations. Developed for the **EcoInnovators 2026** initiative, this platform leverages high-resolution satellite imagery and advanced deep learning models to ensure the integrity of solar deployment under the *PM Surya Ghar: Muft Bijli Yojana*.

By automating the audit process, SolarSight AI eliminates the inefficiencies of manual inspections, providing a scalable, transparent, and highly accurate solution for governance and subsidy monitoring.

---

## 🚀 Key Capabilities

### 📡 Automated Intelligence
Our system automatically interfaces with high-definition satellite providers to fetch localized imagery based on GPS coordinates.

### 🔍 Dual-Stage AI Diagnostics
- **Detection (YOLOv8):** Instant classification and localization of solar arrays with confidence scoring.
- **Segmentation (YOLOv8-Seg):** Precise pixel-level mapping of solar panels to calculate the exact installed area.

### 📊 Audit-Ready Reporting
Every verification run produces a comprehensive digital footprint:
- **Visual Overlays:** High-contrast masks overlaid on satellite imagery for human review.
- **Structured Data:** Detailed JSON outputs containing area metrics, confidence levels, and QC timestamps.
- **Quality Assurance:** Automated "VERIFIABLE" vs "NOT VERIFIABLE" status based on image clarity and detection certainty.

---

## 🛠 Technical Architecture

| Component | Technology |
|---|---|
| **Core AI** | YOLOv8 (Detection & Segmentation) |
| **Framework** | Ultralytics, PyTorch |
| **Dashboard** | Streamlit (Python-based Web UI) |
| **Image Engine** | Google Static Maps API |
| **Logic Layer** | Python 3.10 |

---

## 📦 Project Structure

```bash
SolarSightAI/
├── app.py                # Streamlit Web Dashboard
├── pipeline/             # Core AI Pipeline Modules
│   ├── fetch.py          # Satellite Image Extraction
│   ├── detect.py         # AI Detection Logic
│   ├── pipeline.py       # Orchestration Layer
│   └── ...               # Supplementary Utilities
├── trained_model/        # Production-grade Weights (.pt)
├── assets/               # Branding & Documentation Images
├── output/               # Generated Audit Artifacts
└── requirements.txt      # Dependency Specification
```

---

## 🚦 Getting Started

### 1. Prerequisites
Ensure you have Python 3.10+ installed. You will also need a Google Maps API Key for satellite image fetching.

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/akash14102006/Solar_panel_verification.git
cd Solar_panel_verification
pip install -r requirements.txt
```

### 3. Launch the Dashboard
Run the interactive Streamlit application:
```bash
streamlit run app.py
```

---

## 🔮 Future Roadmap (The "Gemini" Vision)
We are currently exploring integrations with **Google Gemini** to:
- Generate automated, natural-language audit reports for each installation.
- Provide descriptive reasoning for "NOT VERIFIABLE" flags (e.g., "Tree coverage obstructing 40% of the array").
- Implement visual question-answering (VQA) for edge-case diagnostics.

---

## 👥 Meet the Team
**Team:** Health Coder  
**Challenge:** EcoInnovators 2026  
**Lead Developers:** [Akash M](https://github.com/akash14102006), [Mohan Kumar]  
**Contact:** 240769.it@rmkec.ac.in

---

## 📄 License
This project is developed for the EcoInnovators Ideathon 2026. All rights reserved for research and governance applications.
