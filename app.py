import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
import io
import base64
import json

st.set_page_config(layout="wide")
st.title("🏫️ Try a Pouf in Your Room!")

# Load pouf image
pouf_image = Image.open("assets/pouf1.png").convert("RGBA")

# Sidebar scale
st.sidebar.header("🫑 Adjust Pouf")
scale = st.sidebar.slider("Scale %", 20, 500, 100)

# Declare JS component
click_image = components.declare_component("click_image", path=None)

# Upload room image
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    room_image = Image.open(uploaded_file).convert("RGBA")

    display_width = 900
    aspect_ratio = room_image.height / room_image.width
    display_height = int(display_width * aspect_ratio)

    # Resize and convert to base64
    resized_image = room_image.resize((display_width, display_height))
    buf = io.BytesIO()
    resized_image.save(buf, format="PNG")
    base64_img = base64.b64encode(buf.getvalue()).decode()

    # Call JS click component
    coords = click_image(
        key="clicker",
        default=None,
        html=f"""
        <img id="clickable-image" src="data:image/png;base64,{base64_img}"
             width="{display_width}" height="{display_height}" style="cursor:crosshair;" />
        <script>
        const img = window.parent.document.getElementById("clickable-image");
        if (img) {{
            img.onclick = function(e) {{
                const rect = img.getBoundingClientRect();
                const x = Math.round(e.clientX - rect.left);
                const y = Math.round(e.clientY - rect.top);
                const payload = {{x: x, y: y, width: img.width, height: img.height}};
                const streamlitEvent = new CustomEvent("streamlit:componentValue", {{
                    detail: {{ returnValue: payload }}
                }});
                window.parent.dispatchEvent(streamlitEvent);
            }};
        }}
        </script>
        """,
        height=display_height + 60
    )

    if coords and "x" in coords:
        st.success(f"Clicked at ({coords['x']}, {coords['y']})")

        # Map click to original image
        scale_x = room_image.width / coords["width"]
        scale_y = room_image.height / coords["height"]
        x_pos = int(coords["x"] * scale_x)
        y_pos = int(coords["y"] * scale_y)

        # Resize pouf
        new_size = (int(pouf_image.width * scale / 100), int(pouf_image.height * scale / 100))
        scaled_pouf = pouf_image.resize(new_size)

        # Overlay
        overlay = Image.new("RGBA", room_image.size, (255, 255, 255, 0))
        overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)
        result = Image.alpha_composite(room_image, overlay)

        st.image(result, caption="Your Room with Pouf", use_column_width=True)

        # Download
        buf = io.BytesIO()
        result.save(buf, format="PNG")
        st.download_button("📥 Download Image", buf.getvalue(), "your_room_with_pouf.png", "image/png")
    else:
        st.info("🖱️ Click the image to place your pouf.")
else:
    st.info("📤 Upload a room photo to begin.")
