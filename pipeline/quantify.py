import math

CONF_THRESHOLD = 0.50
MIN_AREA_SQM = 0.5
MIN_MASK_PIXELS = 50


def meters_per_pixel(lat_deg, zoom, scale):
    lat_rad = math.radians(lat_deg)
    mpp = (156543.03392 * math.cos(lat_rad)) / (2 ** zoom)
    return mpp / scale


def compute_area_sqm(pixel_count, lat, zoom, scale):
    mpp = meters_per_pixel(lat, zoom, scale)
    return pixel_count * (mpp ** 2)


def qc_decision(has_solar, confidence, sqm, mask_pixels):
    if not has_solar:
        return "NOT_VERIFIABLE"
    if confidence < CONF_THRESHOLD:
        return "NOT_VERIFIABLE"
    if sqm < MIN_AREA_SQM or mask_pixels < MIN_MASK_PIXELS:
        return "NOT_VERIFIABLE"
    return "VERIFIABLE"
