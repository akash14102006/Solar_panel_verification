import os
import json
import cv2
import numpy as np
from datetime import date

OUT_JSON = os.path.join("output", "json")
OUT_OVERLAY = os.path.join("output", "overlay")
os.makedirs(OUT_JSON, exist_ok=True)
os.makedirs(OUT_OVERLAY, exist_ok=True)


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

    with open(os.path.join(OUT_JSON, f"{sample_id}.json"), "w") as f:
        json.dump(data, f, indent=4)

    print("💾 Saved JSON.")


def save_overlay(image_path, mask, bbox_list, polygon, sample_id):
    img = cv2.imread(image_path)

    if bbox_list:
        for x1, y1, x2, y2 in bbox_list:
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    if mask is not None:
        mask_u8 = (mask * 255).astype(np.uint8)

        # Resize mask to image size
        mask_resized = cv2.resize(mask_u8, (img.shape[1], img.shape[0]))

        # Convert to color heatmap
        colored = cv2.applyColorMap(mask_resized, cv2.COLORMAP_JET)

        # Blend mask + image
        img = cv2.addWeighted(img, 0.7, colored, 0.3, 0)

    if polygon:
        pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 255, 255), 2)

    out_path = os.path.join(OUT_OVERLAY, f"{sample_id}.png")
    cv2.imwrite(out_path, img)
    print("🖼 Saved overlay.")
