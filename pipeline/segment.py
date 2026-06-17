import numpy as np
import cv2
import logging
from pathlib import Path
from ultralytics import YOLO
import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
SEGMENT_MODEL_PATH = BASE_DIR / "trained_model" / "best_segment.pt"

@st.cache_resource(show_spinner=False)
def load_segment_model():
    if SEGMENT_MODEL_PATH.exists():
        logger.info(f"Loading segment model from {SEGMENT_MODEL_PATH}")
        return YOLO(str(SEGMENT_MODEL_PATH))
    logger.error(f"Segment model not found at {SEGMENT_MODEL_PATH}")
    return None


def run_segment(image_path: str):
    """
    Returns:
        mask (H,W) binary (0/1)
        pixel_count (int)
    """
    segment_model = load_segment_model()
    if segment_model is None:
        logger.warning("⚠ No segment model found.")
        return None, 0

    logger.info(f"Running segmentation on {image_path}")
    results = segment_model(image_path)[0]
    if results.masks is None:
        return None, 0

    masks = results.masks.data.cpu().numpy()
    idx = int(np.argmax([m.sum() for m in masks]))

    mask = masks[idx].astype(np.uint8)
    pixels = int(mask.sum())
    return mask, pixels


def mask_to_polygon(mask):
    """Convert mask → polygon coordinates."""
    mask_u8 = (mask * 255).astype(np.uint8)
    contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    contour = max(contours, key=cv2.contourArea)
    epsilon = 0.01 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    return [[int(p[0][0]), int(p[0][1])] for p in approx]
