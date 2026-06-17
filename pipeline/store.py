import json
import cv2
import numpy as np
import logging
from datetime import date
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_JSON = BASE_DIR / "output" / "json"
OUT_OVERLAY = BASE_DIR / "output" / "overlay"
OUT_JSON.mkdir(parents=True, exist_ok=True)
OUT_OVERLAY.mkdir(parents=True, exist_ok=True)


def save_json(sample_id, lat, lon, has_solar, conf, sqm, qc, bbox_list, polygon):
    data = {
        "sample_id": sample_id,
        "lat": lat,
        "lon": lon,
        "has_solar": has_solar,
        "confidence": round(conf, 3),
        "pv_area_sqm_est": round(sqm, 3),
        "buffer_radius_sqft": 1200,
        "qc_status": qc,
        "bbox_or_mask": None,
        "image_metadata": {
            "source": "Google Static Maps",
            "capture_date": str(date.today())
        }
    }

    if polygon:
        data["bbox_or_mask"] = {"type": "polygon", "coordinates": polygon}
    elif bbox_list:
        data["bbox_or_mask"] = {"type": "bbox", "bbox": bbox_list[0]}

    out_path = OUT_JSON / f"{sample_id}.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"💾 Saved JSON to {out_path}")


def save_overlay(image_path, mask, bbox_list, polygon, sample_id):
    img = cv2.imread(str(image_path))
    if img is None:
        logger.error(f"Failed to read image at {image_path}")
        return

    if bbox_list:
        for x1, y1, x2, y2 in bbox_list:
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    if mask is not None:
        mask_u8 = (mask * 255).astype(np.uint8)
        mask_resized = cv2.resize(mask_u8, (img.shape[1], img.shape[0]))
        colored = cv2.applyColorMap(mask_resized, cv2.COLORMAP_JET)
        img = cv2.addWeighted(img, 0.7, colored, 0.3, 0)

    if polygon:
        pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 255, 255), 2)

    out_path = OUT_OVERLAY / f"{sample_id}.png"
    cv2.imwrite(str(out_path), img)
    logger.info(f"🖼 Saved overlay to {out_path}")
