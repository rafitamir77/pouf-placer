import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
import io
import base64
import json

st.set_page_config(layout="wide")
st.title("🛋️ Try a Pouf in Your Room!")

# Load pouf image
pouf_image = Image.open("assets/pouf1.png").convert("RGBA")

# Sidebar
st.sidebar.header("🪑 Adjust Pouf")
scale = st.sidebar.slider("Scale %", 20, 500, 100)

# Upload
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    room_image = Image.open(uploaded_file).convert("RGBA")
    display_width = 900
    aspect_ratio = room_image.height / room_image.width
    display_height = int(display_width * aspect_ratio)
    resized_image = room_image.resize((display_width, display_height))

    # Convert to base64
    buffered = io.BytesIO()
    resized_image.save(buffered, format="PNG")
    base64_img = base64.b64encode(buffered.getvalue()).decode()

    # Render image and capture clicks
    components.html(f"""
        <div style="position: relative; width: {display_width}px; height: {display_height}px;">
            <img id="room_image" src="data:image/png;base64,{base64_img}" 
                 width="{display_width}" height="{display_height}" style="cursor: crosshair;">
        </div>
        <script>
        const img = document.getElementById("room_image");
        if (img) {{
            img.onclick = function(e) {{
                const rect = img.getBoundingClientRect();
                const x = Math.round(e.clientX - rect.left);
                const y = Math.round(e.clientY - rect.top);
                const payload = {{ x: x, y: y }};
                console.log("📍 Clicked at:", payload);
                const streamlitEvent = new CustomEvent("streamlit:rendered", {{
                    detail: {{
                        messageType: "streamlit:customClick",
                        value: JSON.stringify(payload)
                    }}
                }});
                window.parent.document.dispatchEvent(streamlitEvent);
            }}
        }}
        </script>
    """, height=display_height + 50)

    # Use Streamlit's input method for JS → Python (use streamlit_js_eval package if needed)
    st.warning("⚠️ To fully support JS to Python click transfer, install `streamlit_js_eval` or switch to custom components.")
    st.code("pip install streamlit_js_eval")

    st.stop()  # Prevent error until streamlit_js_eval or custom JS component is integrated
else:
    st.info("📤 Upload an image to get started.")
