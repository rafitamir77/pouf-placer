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

    # Resize for canvas display
    max_display_width = 800
    aspect_ratio = room_image.height / room_image.width
    display_width = min(room_image.width, max_display_width)
    display_height = int(display_width * aspect_ratio)
    resized_room = room_image.resize((display_width, display_height))

    # Sidebar: Scale slider
    st.sidebar.header("🪑 Adjust Pouf")
    scale = st.sidebar.slider("Scale %", 20, 500, 100)

    # Canvas with resized image
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=0,
        stroke_color="white",
        background_image=resized_room.convert("RGB"),
        update_streamlit=True,
        height=display_height,
        width=display_width,
        drawing_mode="point",
        key="canvas",
    )

    # If user clicked
    if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
        last_click = canvas_result.json_data["objects"][-1]
        x_scaled = int(last_click["left"])
        y_scaled = int(last_click["top"])

        # Map to original image coordinates
        scale_x = room_image.width / display_width
        scale_y = room_image.height / display_height
        x_pos = int(x_scaled * scale_x)
        y_pos = int(y_scaled * scale_y)

        # Resize pouf
        new_size = (int(pouf_image.width * scale / 100), int(pouf_image.height * scale / 100))
        scaled_pouf = pouf_image.resize(new_size)

        # Create overlay and combine
        overlay = Image.new("RGBA", room_image.size, (255, 255, 255, 0))
        overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)
        result = Image.alpha_composite(room_image, overlay)

        # Show result
        st.image(result, caption="Preview with Pouf", use_column_width=True)

        # Download
        buf = io.BytesIO()
        result.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button("📥 Download Image", byte_im, "your_room_with_pouf.png", "image/png")

    else:
        st.info("Click on the image to place your pouf.")
