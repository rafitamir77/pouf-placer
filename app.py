import streamlit as st
from PIL import Image
import numpy as np
import io
from streamlit_drawable_canvas import st_canvas

st.set_page_config(layout="wide")
st.title("🛋️ Try a Pouf in Your Room!")

# Load pouf image
pouf_image = Image.open("assets/pouf1.png").convert("RGBA")

# Upload room photo
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load original image
    room_image = Image.open(uploaded_file).convert("RGBA")

    # Resize for canvas disp
