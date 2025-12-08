import numpy as np
import os
from ultralytics import YOLO

DETECT_MODEL_PATH = os.path.join("trained_model", "best_detect.pt")
detect_model = YOLO(DETECT_MODEL_PATH) if os.path.exists(DETECT_MODEL_PATH) else None


def run_detect(image_path: str):
    """
    Returns:
        has_solar (bool)
        confidence (float)
        bbox_list = [[x1,y1,x2,y2]]
    """
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
