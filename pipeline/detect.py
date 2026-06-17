import numpy as np
import logging
from pathlib import Path
try:
    import cv2
    print("OpenCV loaded:", cv2.__version__)
except Exception as e:
    print("CV2 ERROR:", repr(e))
    raise

from ultralytics import YOLO
import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DETECT_MODEL_PATH = BASE_DIR / "trained_model" / "best_detect.pt"

@st.cache_resource(show_spinner=False)
def load_detect_model():
    if DETECT_MODEL_PATH.exists():
        logger.info(f"Loading detect model from {DETECT_MODEL_PATH}")
        return YOLO(str(DETECT_MODEL_PATH))
    logger.error(f"Detect model not found at {DETECT_MODEL_PATH}")
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
        logger.warning("⚠ No detection model found.")
        return False, 0.0, None

    logger.info(f"Running detection on {image_path}")
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
