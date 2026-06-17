import os
import requests
import logging
from datetime import date
from pathlib import Path

try:
    import streamlit as st
except ImportError:
    st = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
if not API_KEY and st is not None:
    try:
        API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]
    except Exception:
        pass
if not API_KEY:
    API_KEY = "AIzaSyBWaOJbGUY8pX0VolJmC7qthqmHa-voIV0"

ZOOM = 20
SCALE = 2
IMG_SIZE = 640

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_ROOT = BASE_DIR / "output"
OUT_ROOT.mkdir(parents=True, exist_ok=True)

def fetch_image(lat: float, lon: float, sample_id: int):
    """
    Download high-zoom Google Satellite map image.
    Saves → output/{sample_id}_input.png
    """
    url = (
        "https://maps.googleapis.com/maps/api/staticmap?"
        f"center={lat},{lon}&zoom={ZOOM}&size={IMG_SIZE}x{IMG_SIZE}&scale={SCALE}"
        f"&maptype=satellite&key={API_KEY}"
    )

    out_path = OUT_ROOT / f"{sample_id}_input.png"

    try:
        r = requests.get(url, timeout=30)
    except Exception as e:
        logger.error(f"❌ Fetch exception: {e}")
        raise RuntimeError(f"Failed to connect to Google Maps API: {e}")

    if r.status_code != 200:
        error_msg = f"Google API error {r.status_code}: {r.text[:200]}"
        logger.error(f"❌ {error_msg}")
        raise RuntimeError(error_msg)

    with open(out_path, "wb") as f:
        f.write(r.content)

    logger.info(f"✅ Image saved → {out_path}")
    return str(out_path)
