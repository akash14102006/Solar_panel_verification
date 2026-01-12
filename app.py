import streamlit as st
import json
import os
from pipeline.pipeline import run

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="SolarSight – Rooftop Solar Verification",
    layout="wide"
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(
    """
    <h1 style="text-align:center; color:#2E7D32;">
        SolarSight Verification System
    </h1>
    <h4 style="text-align:center; color:#6B7280;">
        Rooftop Solar Verification Platform
    </h4>
    <hr>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# MAIN LAYOUT
# -------------------------------------------------
left_col, right_col = st.columns([1, 2])

# =========================
# LEFT — INPUT PANEL
# =========================
with left_col:
    st.markdown("## Input Coordinates")

    st.markdown(
        """
        <div style="background:#F5F7FA; padding:18px; border-radius:10px;">
        """,
        unsafe_allow_html=True
    )

    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    sample_id = st.number_input("Sample ID", min_value=1, step=1)

    run_button = st.button("Run Solar Verification", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# RIGHT — RESULTS
# =========================
with right_col:
    st.markdown("## Verification Results")

    if run_button:
        with st.spinner("Running AI verification pipeline..."):
            run(sample_id, lat, lon)

        st.success("Verification completed successfully.")

        img_path = f"output/{sample_id}_input.png"
        overlay_path = f"output/overlay/{sample_id}.png"
        json_path = f"output/json/{sample_id}.json"

        # ---------- COMPACT RESULT GRID ----------
        col_img, col_overlay, col_json = st.columns([1, 1, 1])

        # ---- Satellite Image (SMALL) ----
        with col_img:
            st.markdown("### Satellite Image")
            if os.path.exists(img_path):
                st.image(img_path, width=250)
            else:
                st.warning("Not available")

        # ---- Detection Overlay (SMALL) ----
        with col_overlay:
            st.markdown("### Detection Overlay")
            if os.path.exists(overlay_path):
                st.image(overlay_path, width=250)
            else:
                st.warning("Not available")

        # ---- JSON Output (COMPACT) ----
        with col_json:
            st.markdown("### AI Output")

            if os.path.exists(json_path):
                with open(json_path) as f:
                    data = json.load(f)

                # QC badge
                if data.get("qc_status") == "VERIFIABLE":
                    st.success("QC STATUS: VERIFIABLE")
                else:
                    st.error("QC STATUS: NOT VERIFIABLE")

                st.code(json.dumps(data, indent=2), language="json")
            else:
                st.warning("JSON not found")
