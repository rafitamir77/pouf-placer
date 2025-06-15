import streamlit as st
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas
import numpy as np  # <-- Make sure this is imported

st.set_page_config(page_title="Image Canvas", layout="wide")

st.title("🖼️ Upload an Image and Draw on It")

uploaded_file = st.file_uploader("📷 Upload image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")


    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="red",
        background_image=image, 
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        display_toolbar=False,
        key="canvas"
    )
else:
    st.info("⬆️ Upload a .jpg or .png image to begin drawing.")
