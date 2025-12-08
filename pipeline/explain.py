def explain(has_solar, conf, polygon, bbox):
    if polygon:
        return "Polygon mask successfully generated."
    if bbox:
        return "Bounding box detected."
    if not has_solar:
        return "No solar detected due to obstruction or low clarity."
    return "No explanation available."
