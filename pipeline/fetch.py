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

API_KEY = os.environ.get("MAPTILER_API_KEY")
if not API_KEY and st is not None:
    try:
        API_KEY = st.secrets.get("MAPTILER_API_KEY")
    except Exception:
        pass
if not API_KEY:
    API_KEY = "Cn83bhjCz5TGAZx6TQM5"

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_ROOT = BASE_DIR / "output"
OUT_ROOT.mkdir(parents=True, exist_ok=True)

def fetch_image(lat: float, lon: float, sample_id: int):
    """
    Download high-zoom MapTiler Satellite map image.
    Saves → output/{sample_id}_input.jpg
    """
    url = f"https://api.maptiler.com/maps/satellite-v4/static/{lon},{lat},19/640x640.jpg?key={API_KEY}"

    print(lat)
    print(lon)
    print(url)

    out_path = OUT_ROOT / f"{sample_id}_input.jpg"

    try:
        r = requests.get(url, timeout=30)
    except Exception as e:
        logger.error(f"❌ Fetch exception: {e}")
        raise RuntimeError(f"Failed to connect to MapTiler API: {e}")

    print(r.status_code)

    if r.status_code != 200:
        error_msg = f"MapTiler API error {r.status_code}: {r.text[:200]}"
        logger.error(f"❌ {error_msg}")
        raise RuntimeError(error_msg)
        
    if len(r.content) == 0:
        error_msg = f"MapTiler API returned empty image."
        logger.error(f"❌ {error_msg}")
        raise RuntimeError(error_msg)

    with open(out_path, "wb") as f:
        f.write(r.content)

    logger.info(f"✅ Image saved → {out_path}")
    return str(out_path)
