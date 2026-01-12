# Solar_panel_verification

📌 1. Project Overview
Solar panel verification an end-to-end automated verification pipeline designed to validate rooftop solar photovoltaic (PV) installations under the PM Surya Ghar: Muft Bijli Yojana.

Using satellite imagery + YOLOv8 AI models, the system:

Detects whether a solar panel exists at a given location

Generates polygon masks (for segmentation)

Estimates the installed rooftop solar area

Produces audit-ready JSON + PNG overlays

Assigns QC status (VERIFIABLE / NOT_VERIFIABLE)

Ensures transparency for large-scale subsidy monitoring

This reduces the need for manual inspection, enabling faster, cheaper, and scalable verification across India.

📌 2. Features
✔ Automated Image Fetching
Fetches high-resolution satellite images using Google Static Maps API.

✔ Solar Panel Detection (YOLOv8-Detection)
YES/NO classification with bounding box & confidence score.

✔ Solar Panel Segmentation (YOLOv8-Segmentation)
Generates polygon masks + area estimation in m².

✔ Quality Check System
Rules-based QC to determine if the result is usable.

✔ Audit-Ready Outputs
Produces:

/output/json/sample_id.json

/output/overlay/sample_id.png

✔ Generalizes Across Indian Roof Types
Tin roofs, cement slabs, tiled houses, rural & urban structures.

📌 3. Repository Structure
pgsql
Copy code
Solar_panel_verification/
│
├── pipeline/
│   ├── pipeline.py
│   ├── fetch.py
│   ├── detect.py
│   ├── segment.py
│   ├── quantify.py
│   ├── explain.py
│   ├── store.py
│
├── trained_model/
│   ├── best_detect.pt
│   ├── best_segment.pt
│   ├── model_card.pdf
│
├── output/
│   ├── json/
│   ├── overlay/
│   ├── sample_input.png
│
├── requirements.txt
├── README.md
└── test.py

📌 4. Tech Stack
Component	Technology
AI Models	YOLOv8 Detection + Segmentation
Framework	Ultralytics, PyTorch
Programming Language	Python 3.10
Image Fetching	Google Static Maps API
Storage Format	JSON, PNG Overlays
Training	Google Colab (T4 GPU)

📌 5. Models Used
Model 1 — best_detect.pt
Task: Solar panel presence detection

Output: Bounding box + confidence

Metric: F1 ≈ 0.82

Model 2 — best_segment.pt
Task: Pixel-level solar segmentation

Output: Mask + panel area

Metric: mAP50 ≈ 0.78

📌 6. Limitations
Tree cover may hide panels

Very old / low resolution imagery may reduce accuracy

Water tanks & metal roofs may cause false positives

Not suitable for real-time drone inspections

📌 7. Future Enhancements
Add transformer-based detection (SAM / SegFormer)

Build mobile or web dashboard for DISCOMs

Integrate historical imagery for trend analysis

Automatic rooftop boundary detection

📌 8. Team
Team Name: Health Coder 
Challenge: EcoInnovators 2026 – Rooftop Solar Verification
Members: Akash M , Mohan Kumar
Email: 240769.it@rmkec.ac.in

📌 11. License
This project is developed for EcoInnovators Ideathon 2026 and is intended for research & governance use only.
