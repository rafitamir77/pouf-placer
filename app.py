import streamlit as st
from PIL import Image, ImageOps
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
    # Fix orientation and convert to RGBA
    room_image = ImageOps.exif_transpose(Image.open(uploaded_file)).convert("RGBA")

    # Resize for canvas display
    max_display_width = 900
    aspect_ratio = room_image.height / room_image.width
    display_width = min(room_image.width, max_display_width)
    display_height = int(display_width * aspect_ratio)
    if "last_image" in st.session_state:
        resized_room = st.session_state["last_image"].resize((display_width, display_height))
    else:
        resized_room = room_image.resize((display_width, display_height))

    # Convert resized image to NumPy RGB array (✅ required for canvas)
    background_rgb = resized_room.convert("RGB")

    # Sidebar controls
    st.sidebar.header("🪑 Adjust Pouf")
    scale = st.sidebar.slider("Scale %", 20, 500, 100)
    if st.sidebar.button("🔄 Reset Canvas"):
        if "last_image" in st.session_state:
            del st.session_state["last_image"]


    # Canvas
    st.info("🖱️ Click on the image below to place your pouf.")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=0,
        stroke_color="white",
        background_image=background_rgb,
        update_streamlit=True,
        height=display_height,
        width=display_width,
        drawing_mode="point",
        key="canvas"
    )
    # If user clicked
    if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
        last_click = canvas_result.json_data["objects"][-1]
        x_scaled = int(last_click["left"])
        y_scaled = int(last_click["top"])

        # Map click to original image
        scale_x = room_image.width / display_width
        scale_y = room_image.height / display_height
        x_pos = int(x_scaled * scale_x)
        y_pos = int(y_scaled * scale_y)

        # Resize pouf
        new_size = (int(pouf_image.width * scale / 100), int(pouf_image.height * scale / 100))
        scaled_pouf = pouf_image.resize(new_size)

        # Place pouf
        overlay = Image.new("RGBA", room_image.size, (255, 255, 255, 0))
        overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)
        result = Image.alpha_composite(room_image, overlay)
        background_rgb_new = result.convert("RGB")

        # Show result
        #st.markdown("### 🖼️ Result Preview")
        #st.image(result, use_column_width=True)
        st.session_state["last_image"] = result
        
        st.experimental_rerun()

        # Download
        buf = io.BytesIO()
        result.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button("📥 Download Image", byte_im, "your_room_with_pouf.png", "image/png")

