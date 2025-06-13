import streamlit as st
from PIL import Image
import numpy as np
import io
from streamlit_drawable_canvas import st_canvas

st.set_page_config(layout="wide")
st.title("🛋️ Try a Pouf in Your Room!")
scale = st.sidebar.slider("Scale %", 20, 500, 100)

# Load pouf
pouf_image = Image.open("assets/pouf1.png").convert("RGBA")

uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load and prepare image
    room_image = Image.open(uploaded_file).convert("RGBA")
    room_width, room_height = room_image.size

    background_np = room_image.convert("RGB")

    # Canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=0,
        stroke_color="white",
        background_image=background_np,  # ✅ only assigned if uploaded_file is valid
        update_streamlit=True,
        height=room_height,
        width=room_width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
        last_click = canvas_result.json_data["objects"][-1]
        x_pos = int(last_click["left"])
        y_pos = int(last_click["top"])

        # Resize pouf
        new_size = (int(pouf_image.width * scale / 100), int(pouf_image.height * scale / 100))
        scaled_pouf = pouf_image.resize(new_size)

        # Paste on transparent overlay
        overlay = Image.new("RGBA", room_image.size, (255, 255, 255, 0))
        overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)

        result = Image.alpha_composite(room_image, overlay)

        st.image(result, caption="Preview with Pouf", use_column_width=True)

        buf = io.BytesIO()
        result.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(label="📥 Download Image", data=byte_im, file_name="your_room_with_pouf.png", mime="image/png")
    else:
        st.info("Click anywhere on the image to place your pouf.")
