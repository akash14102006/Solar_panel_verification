import numpy as np
import os
try:
    import cv2
    print("OpenCV loaded:", cv2.__version__)
except Exception as e:
    print("CV2 ERROR:", repr(e))
    raise

from ultralytics import YOLO
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DETECT_MODEL_PATH = os.path.join(PROJECT_ROOT, "trained_model", "best_detect.pt")

@st.cache_resource(show_spinner=False)
def load_detect_model():
    if os.path.exists(DETECT_MODEL_PATH):
        return YOLO(DETECT_MODEL_PATH)
    return None


def run_detect(image_path: str):
    """
    Returns:
        has_solar (bool)
        confidence (float)
        bbox_list = [[x1,y1,x2,y2]]
    """
    detect_model = load_detect_model()
    if detect_model is None:
        print("⚠ No detection model found.")
        return False, 0.0, None

    results = detect_model(image_path)[0]
    boxes = results.boxes

    if boxes is None or len(boxes) == 0:
        return False, 0.0, None

    best_idx = int(np.argmax([b.conf.cpu().numpy() for b in boxes]))
    best = boxes[best_idx]

    conf = float(best.conf)
    xyxy = best.xyxy.cpu().numpy().tolist()

    if isinstance(xyxy[0], (list, tuple)):
        bbox_list = xyxy
    else:
        bbox_list = [xyxy]

    return True, conf, bbox_list
