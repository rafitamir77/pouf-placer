import streamlit as st
from PIL import Image
import cv2
import numpy as np
import io

st.set_page_config(layout="wide")
st.title("🛋️ Try a Pouf in Your Room!")

# Load pouf
pouf_image = Image.open("assets/pouf1.png").convert("RGBA")

uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load room image
    room_image = Image.open(uploaded_file).convert("RGBA")

    # Resize pouf to match room scale (arbitrary default)
    base_pouf = pouf_image.resize((500, 500))

    # Let user drag pouf (simple x/y sliders)
    st.sidebar.header("🪑 Adjust Pouf Placement")
    x_pos = st.sidebar.slider("Horizontal (X)", 0, room_image.width, int(room_image.width / 2))
    y_pos = st.sidebar.slider("Vertical (Y)", 0, room_image.height, int(room_image.height / 2))
    scale = st.sidebar.slider("Scale %", 20, 500, 100)

    # Scale pouf
    new_size = (int(base_pouf.width * scale / 100), int(base_pouf.height * scale / 100))
    scaled_pouf = base_pouf.resize(new_size)

    # Create transparent overlay
    room_array = np.array(room_image)
    pouf_array = np.array(scaled_pouf)

    # Place pouf in blank canvas
    overlay = Image.new("RGBA", room_image.size, (255, 255, 255, 0))
    overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)

    # Combine
    result = Image.alpha_composite(room_image, overlay)

    st.image(result, caption="Preview with Pouf", use_column_width=True)

    # Download option
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(label="📥 Download Image", data=byte_im, file_name="your_room_with_pouf.png", mime="image/png")

