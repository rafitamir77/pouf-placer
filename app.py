import streamlit as st
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas

# Streamlit page config
st.set_page_config(
    page_title="Image Canvas",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🖼️ Upload an Image and Draw on It")

# Upload section
uploaded_file = st.file_uploader("📷 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Load and fix image orientation
    image = ImageOps.exif_transpose(Image.open(uploaded_file)).convert("RGB")

    # Resize for canvas
    max_width = 500
    aspect_ratio = image.height / image.width
    display_width = min(image.width, max_width)
    display_height = int(display_width * aspect_ratio)
    resized_image = image.resize((display_width, display_height))

    # Show debug info
    st.write(f"Image size: {image.size}")
    st.write(f"Canvas size: {display_width} x {display_height}")

    st.image(resized_image, caption="📷 Preview", use_column_width=False)

    st.markdown("### ✏️ Draw on the Image Below")

    # Draw canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="black",
        background_image=resized_image.convert("RGB"),
        update_streamlit=True,
        height=display_height,
        width=display_width,
        drawing_mode="freedraw",  # Or "line", "rect", "circle", "point"
        key="canvas"
    )

    # Optionally show JSON of drawing
    if canvas_result.json_data:
        st.subheader("🧠 Canvas Data (Optional Debug)")
        st.json(canvas_result.json_data)
else:
    st.info("⬆️ Upload a .jpg or .png image to get started.")
