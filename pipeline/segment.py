import os
import numpy as np
import cv2
from ultralytics import YOLO
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SEGMENT_MODEL_PATH = os.path.join(PROJECT_ROOT, "trained_model", "best_segment.pt")

@st.cache_resource(show_spinner=False)
def load_segment_model():
    if os.path.exists(SEGMENT_MODEL_PATH):
        return YOLO(SEGMENT_MODEL_PATH)
    return None


def run_segment(image_path: str):
    """
    Returns:
        mask (H,W) binary (0/1)
        pixel_count (int)
    """
    segment_model = load_segment_model()
    if segment_model is None:
        return None, 0

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
