import streamlit as st
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas

st.set_page_config(layout="wide")
st.title("🛋️ Try a Pouf in Your Room!")

# Upload room photo
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Load and fix orientation
    image = ImageOps.exif_transpose(Image.open(uploaded_file)).convert("RGB")

    # Resize image to max 500px wide
    max_width = 500
    aspect = image.height / image.width
    width = min(image.width, max_width)
    height = int(width * aspect)
    resized = image.resize((width, height))

    # Debug: show the image
    st.image(resized, caption="Resized background image")

    # ✅ This must be a PIL.Image in RGB mode
    background_image = resized

    st.info("🖱️ Click on the image to place a pouf.")
    canvas_result = st_canvas(
        background_image=background_image,  # ✅ RGB PIL.Image
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="point",
        stroke_width=0,
        stroke_color="white",
        fill_color="rgba(255, 165, 0, 0.3)",
        key="canvas",
        display_toolbar=False,
        point_display_radius=1  # optional
    )

    # Optional: inspect click
    if canvas_result.json_data and canvas_result.json_data.get("objects"):
        st.write("📍 Clicked at:", canvas_result.json_data["objects"][-1])
else:
    st.warning("👆 Please upload a room photo to get started.")
