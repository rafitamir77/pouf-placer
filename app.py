import streamlit as st
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Image Canvas", layout="wide")

st.title("🖼️ Upload an Image and Draw on It")

uploaded_file = st.file_uploader("📷 Upload image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = ImageOps.exif_transpose(Image.open(uploaded_file)).convert("RGB")

    max_width = 500
    aspect_ratio = image.height / image.width
    display_width = min(image.width, max_width)
    display_height = int(display_width * aspect_ratio)

    resized_image = image.resize((display_width, display_height))

    st.image(resized_image, caption="📷 Preview", use_column_width=False)

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="red",
        background_image=resized_image.copy().convert("RGB"),  # ✅ critical
        update_streamlit=True,
        height=display_height,
        width=display_width,
        drawing_mode="freedraw",
        display_toolbar=True,
        key="canvas"
    )
else:
    st.info("⬆️ Upload a .jpg or .png image to begin drawing.")
