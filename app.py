import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
import io
import base64

st.set_page_config(layout="wide")
st.title("🛋️ Try a Pouf in Your Room!")

# Load pouf image
pouf_image = Image.open("assets/pouf1.png").convert("RGBA")

# Upload room image
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "jpeg", "png"])

# Sidebar scale
st.sidebar.header("🪑 Adjust Pouf")
scale = st.sidebar.slider("Scale %", 20, 500, 100)

# Initialize click data
if "click_data" not in st.session_state:
    st.session_state["click_data"] = None

if uploaded_file:
    room_image = Image.open(uploaded_file).convert("RGBA")
    display_width = 900
    aspect_ratio = room_image.height / room_image.width
    display_height = int(display_width * aspect_ratio)

    # Convert to base64 for HTML
    buffered = io.BytesIO()
    resized_image = room_image.resize((display_width, display_height))
    resized_image.save(buffered, format="PNG")
    base64_img = base64.b64encode(buffered.getvalue()).decode()

    # Declare custom Streamlit component to capture click events
    import streamlit.components.v1 as components
    _click_component = components.declare_component("clickable_image", path=None)

    clicked = _click_component(
        image=base64_img,
        width=display_width,
        height=display_height,
        default=None
    )

    components.html(f"""
        <script>
        const imgId = "room_image_custom";
        let img = document.getElementById(imgId);
        if (!img) {{
            img = document.createElement("img");
            img.src = "data:image/png;base64,{base64_img}";
            img.id = imgId;
            img.width = {display_width};
            img.height = {display_height};
            img.style.cursor = "crosshair";
            document.body.appendChild(img);
            img.onclick = function(e) {{
                const rect = img.getBoundingClientRect();
                const x = Math.round(e.clientX - rect.left);
                const y = Math.round(e.clientY - rect.top);
                const payload = {{ x: x, y: y, width: img.width, height: img.height }};
                const jsonStr = JSON.stringify(payload);
                window.parent.postMessage({{
                    isStreamlitMessage: true,
                    type: "streamlit:setComponentValue",
                    value: jsonStr
                }}, "*");
            }}
        }}
        </script>
    """, height=display_height + 60)

    if clicked:
        try:
            import json
            coords = json.loads(clicked)
            x = int(coords["x"])
            y = int(coords["y"])
            w = int(coords.get("width", display_width))
            h = int(coords.get("height", display_height))

            # Map click to original image size
            scale_x = room_image.width / w
            scale_y = room_image.height / h
            x_pos = int(x * scale_x)
            y_pos = int(y * scale_y)

            # Scale pouf
            new_size = (int(pouf_image.width * scale / 100), int(pouf_image.height * scale / 100))
            scaled_pouf = pouf_image.resize(new_size)

            # Overlay pouf
            overlay = Image.new("RGBA", room_image.size, (255, 255, 255, 0))
            overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)
            result = Image.alpha_composite(room_image, overlay)

            st.image(result, caption="Your Room with Pouf", use_column_width=True)

            # Download
            buf = io.BytesIO()
            result.save(buf, format="PNG")
            byte_im = buf.getvalue()
            st.download_button("📥 Download Image", byte_im, "your_room_with_pouf.png", "image/png")
        except Exception as e:
            st.warning(f"⚠️ Error parsing click: {e}")
    else:
        st.info("Click on the image to place the pouf.")

else:
    st.info("Please upload a room photo to get started.")
