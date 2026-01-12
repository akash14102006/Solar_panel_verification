import os
import requests
from datetime import date

API_KEY = "AIzaSyBWaOJbGUY8pX0VolJmC7qthqmHa-voIV0"   # CHANGE THIS
ZOOM = 19
SCALE = 2
IMG_SIZE = 640

OUT_ROOT = os.path.join(os.getcwd(), "output")
os.makedirs(OUT_ROOT, exist_ok=True)


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

    out_path = os.path.join(OUT_ROOT, f"{sample_id}_input.png")

    try:
        r = requests.get(url, timeout=30)
    except Exception as e:
        print("❌ Fetch error:", e)
        return None

    if r.status_code != 200:
        print("❌ Google API error:", r.status_code, r.text[:200])
        return None

    with open(out_path, "wb") as f:
        f.write(r.content)

    print(f"✅ Image saved → {out_path}")
    return out_path
