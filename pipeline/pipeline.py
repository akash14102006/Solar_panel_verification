from pipeline.fetch import fetch_image
from pipeline.detect import run_detect
from pipeline.segment import run_segment, mask_to_polygon
from pipeline.quantify import compute_area_sqm, qc_decision
from pipeline.store import save_json, save_overlay
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ZOOM = 20
SCALE = 2


def run(sample_id, lat, lon):
    logger.info(f"\n=== Running sample {sample_id} ===")

    # Fetch image - will raise RuntimeError if it fails
    img = fetch_image(lat, lon, sample_id)

    # Detect
    has_solar, conf, bbox = run_detect(img)

    # Segmentation
    mask, pix = run_segment(img)

    polygon = None
    sqm = 0.0

    if mask is not None and pix > 0:
        polygon = mask_to_polygon(mask)
        sqm = compute_area_sqm(pix, lat, ZOOM, SCALE)

    qc = qc_decision(has_solar, conf, sqm, pix)

    # Save outputs
    save_json(sample_id, lat, lon, has_solar, conf, sqm, qc, bbox, polygon)
    save_overlay(img, mask, bbox, polygon, sample_id)

    logger.info(f"Done! QC={qc}, Solar={has_solar}, Area={sqm:.2f}sqm\n")
