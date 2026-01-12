import streamlit as st
import json
import os
from pipeline.pipeline import run

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="SolarSight AI – Rooftop Solar Verification",
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
    <h3 style="text-align:center; color:gray;">
    Rooftop Solar Verification Platform
    </h3>
    <hr>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# MAIN DASHBOARD LAYOUT
# -------------------------------------------------
left_col, right_col = st.columns([1, 2])

# =========================
# LEFT SIDE — INPUT PANEL
# =========================
with left_col:
    st.markdown("## Input Coordinates")

    with st.container():
        st.markdown(
            """
            <div style="background-color:#F5F7FA; padding:20px; border-radius:10px;">
            """,
            unsafe_allow_html=True
        )

        lat = st.number_input("Latitude", format="%.6f")
        lon = st.number_input("Longitude", format="%.6f")
        sample_id = st.number_input("Sample ID", min_value=1, step=1)

        run_button = st.button("Run Solar Verification", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# RIGHT SIDE — RESULTS
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

        # -------- Satellite Image --------
        st.markdown("### Satellite Image")
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.warning("Satellite image not available.")

        # -------- Detection Overlay --------
        st.markdown("### Detection Overlay")
        if os.path.exists(overlay_path):
            st.image(overlay_path, use_container_width=True)
        else:
            st.warning("Overlay image not available.")

        # -------- JSON Output --------
        st.markdown("### AI Output (JSON)")
        if os.path.exists(json_path):
            with open(json_path) as f:
                json_data = json.load(f)

            if json_data.get("qc_status") == "VERIFIABLE":
                st.success("QC STATUS: VERIFIABLE")
            else:
                st.error("QC STATUS: NOT VERIFIABLE")

            st.code(json.dumps(json_data, indent=4), language="json")
        else:
            st.warning("JSON output not available.")
