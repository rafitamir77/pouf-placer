import streamlit as st
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Image Canvas", layout="wide")

st.title("🖼️ Upload and Draw on Image")

uploaded_file = st.file_uploader("Upload a JPG or PNG image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Fix image orientation and convert to RGB (no transparency!)
    image = ImageOps.exif_transpose(Image.open(uploaded_file)).convert("RGB")

    # Resize for canvas
    max_display_width = 500
    aspect_ratio = image.height / image.width
    canvas_width = min(image.width, max_display_width)
    canvas_height = int(canvas_width * aspect_ratio)
    image_resized = image.resize((canvas_width, canvas_height)).convert("RGB")

    st.subheader("🖼️ Preview")
    st.image(image_resized, width=canvas_width)

    st.subheader("📝 Draw on Image")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",  # Red with some transparency
        stroke_width=3,
        stroke_color="black",
        background_image=image_resized,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="freedraw",
        key="canvas"
    )

    # Debug JSON
    if canvas_result.json_data:
        st.subheader("🧠 Drawing Data")
        st.json(canvas_result.json_data)

else:
    st.info("👆 Upload an image to start drawing.")
