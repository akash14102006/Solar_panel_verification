# SolarSight AI: Intelligent Rooftop Solar Verification

![SolarSight AI Banner](assets/banner.png)

## Overview
SolarSight AI is a state-of-the-art automated verification pipeline designed to validate rooftop solar photovoltaic (PV) installations. This platform leverages high-resolution satellite imagery and advanced deep learning models to ensure the integrity of solar deployment under the PM Surya Ghar: Muft Bijli Yojana.

By automating the audit process, SolarSight AI eliminates the inefficiencies of manual inspections, providing a scalable, transparent, and highly accurate solution for governance and subsidy monitoring.

---

## Core Capabilities

### Satellite Intelligence
Automated interface with high-definition satellite providers to fetch localized imagery based on precise GPS coordinates.

### Dual-Stage AI Diagnostics
*   **Object Detection:** Instant classification and localization of solar arrays using YOLOv8 with real-time confidence scoring.
*   **Geospatial Segmentation:** Pixel-level mapping to calculate exact installed area and panel orientation.

### Audit-Ready Reporting
Every verification run produces a comprehensive digital footprint:
*   **Visual Overlays:** High-contrast masks overlaid on satellite imagery for human review and validation.
*   **Structured Data:** Structured JSON outputs containing area metrics, confidence levels, and QC timestamps.
*   **Quality Assurance:** Automated validation status based on image clarity and detection certainty.

---

## Technical Architecture

| Component | specification |
|---|---|
| AI Engine | YOLOv8 (Detection & Segmentation) |
| Framework | Ultralytics, PyTorch |
| Web Interface | Streamlit |
| Image Sourcing | Google Static Maps API |
| Environment | Python 3.10 |

---

## Project Structure

```bash
SolarSightAI/
├── app.py                # Streamlit Web Dashboard
├── pipeline/             # Core AI Pipeline Modules
│   ├── fetch.py          # Satellite Image Extraction
│   ├── detect.py         # AI Detection Logic
│   ├── pipeline.py       # Orchestration Layer
├── trained_model/        # Production-grade Weights (.pt)
├── assets/               # Project Assets & Branding
├── output/               # Generated Audit Artifacts
└── requirements.txt      # Dependency Specification
```

---

## Deployment

### Dependencies
Ensure the system environment meets the requirements specified in `requirements.txt`.

### Application Launch
The interactive dashboard can be initiated via the command line:
```bash
streamlit run app.py
```

---

## Future Development
Our current research focuses on integrating LLM capabilities to:
*   Generate natural-language audit reports for each installation.
*   Provide descriptive reasoning for quality control flags (e.g., "Obstruction detected: Tree coverage exceeds 30%").
*   Implement visual question-answering for complex edge-case diagnostics.

---

## Development Team
**Organization:** Health Coder  
**Program:** EcoInnovators 2026 – Rooftop Solar Verification  
**Lead Developers:** Akash M, Mohan Kumar  
**Inquiries:** 240769.it@rmkec.ac.in

---

## Legal
This project is developed for the EcoInnovators Ideathon 2026. Data and methodology are intended for research and governance applications.
