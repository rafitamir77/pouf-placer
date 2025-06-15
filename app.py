import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import io
from streamlit_drawable_canvas import st_canvas


st.set_page_config(layout="wide")
st.title("🛋️ Try a Pouf in Your Room!")

# Load pouf image
pouf_image = Image.open("assets/pouf1.png")
#pouf_image = Image.open("assets/pouf1.png").convert("RGBA")

# Upload room photo
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Fix orientation and convert to RGBA
    room_image = ImageOps.exif_transpose(Image.open(uploaded_file)).convert("RGBA")

    # Resize for canvas display
    max_display_width = 500
    aspect_ratio = room_image.height / room_image.width
    display_width = min(room_image.width, max_display_width)
    display_height = int(display_width * aspect_ratio)
    resized_room = room_image.resize((display_width, display_height))

    st.write(f'aspect_ratio {aspect_ratio}.')
    st.write(f'display_width {display_width}.')
    st.write(f'display_height {display_height}.')
    st.write(f'room_image.width {room_image.width}.')
    st.write(f'room_image.height {room_image.height}.')

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=1,
        stroke_color="white",
        background_image=room_image.convert("RGB"),
        update_streamlit=True,
        height=room_image.height,
        width=room_image.width,
        drawing_mode="point",
        display_toolbar=False,
        key="canvas"
    )


    if "last_image" in st.session_state:
        # Show latest image with pouf
        resized_room = st.session_state["last_image"].resize((display_width, display_height))
    else:
        resized_room = resized_room;
        
    st.image(resized_room, use_column_width=True)

    # Convert resized image to NumPy RGB array (✅ required for canvas)
    background_rgb = resized_room.convert("RGB") 
    #background_rgb = resized_room

    # Sidebar controls
    st.sidebar.header("🪑 Adjust Pouf")
    scale = st.sidebar.slider("Scale %", 20, 500, 100, step=5)
    if st.sidebar.button("🔄 Reset Canvas"):
        if "last_image" in st.session_state:
            del st.session_state["last_image"]

 