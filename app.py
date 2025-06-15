import streamlit as st
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas

st.set_page_config(layout="wide")
st.title("🖼️ Upload an Image and Draw on It")

# Upload image
uploaded_file = st.file_uploader("📷 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Load image and fix orientation
    image = ImageOps.exif_transpose(Image.open(uploaded_file)).convert("RGB")

    # Resize image to fit canvas width
    max_width = 500
    aspect_ratio = image.height / image.width
    display_width = min(image.width, max_width)
    display_height = int(display_width * aspect_ratio)

    resized_image = image.resize((display_width, display_height))

    # Display debug info
    st.write(f"Image size: {image.size}")
    st.write(f"Canvas size: {display_width} x {display_height}")

    # Canvas with uploaded image
    st.markdown("### ✏️ Draw on the Image Below")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Orange fill
        stroke_width=2,
        stroke_color="black",
        background_image=resized_image,
        update_streamlit=True,
        height=display_height,
        width=display_width,
        drawing_mode="freedraw",  # You can change this to "line", "rect", "circle", etc.
        key="canvas"
    )
else:
    st.info("⬆️ Upload an image to get started.")
