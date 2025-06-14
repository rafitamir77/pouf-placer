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

# Sidebar scale
st.sidebar.header("🪑 Adjust Pouf")
scale = st.sidebar.slider("Scale %", 20, 500, 100)

# Upload room photo
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    room_image = Image.open(uploaded_file).convert("RGBA")
    display_width = 900
    aspect_ratio = room_image.height / room_image.width
    display_height = int(display_width * aspect_ratio)
    resized_image = room_image.resize((display_width, display_height))

    # Convert to base64 for embedding in HTML
    buf = io.BytesIO()
    resized_image.save(buf, format="PNG")
    base64_img = base64.b64encode(buf.getvalue()).decode()

    # JavaScript click capture with postMessage
    custom_component = components.html(f"""
        <div>
            <script>
            const img = document.getElementById("room_img");
            if (!img) {{
                const newImg = document.createElement("img");
                newImg.id = "room_img";
                newImg.src = "data:image/png;base64,{base64_img}";
                newImg.style.cursor = "crosshair";
                newImg.width = {display_width};
                newImg.height = {display_height};
                document.body.appendChild(newImg);

                newImg.onclick = function(e) {{
                    const rect = newImg.getBoundingClientRect();
                    const x = Math.round(e.clientX - rect.left);
                    const y = Math.round(e.clientY - rect.top);
                    const data = {{x, y}};
                    const jsonData = JSON.stringify(data);
                    window.parent.postMessage({{
                        isStreamlitMessage: true,
                        type: "streamlit:setComponentValue",
                        value: jsonData
                    }}, "*");
                }};
            }}
            </script>
        </div>
    """, height=display_height + 50)

    # Get click result
    if isinstance(custom_component, str):
        try:
            click_data = json.loads(custom_component)
            x = click_data["x"]
            y = click_data["y"]

            # Map click to original size
            scale_x = room_image.width / display_width
            scale_y = room_image.height / display_height
            x_pos = int(x * scale_x)
            y_pos = int(y * scale_y)

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
            byte_im = buf.getvalue()
            st.download_button("📥 Download Image", byte_im, "your_room_with_pouf.png", "image/png")
        except Exception as e:
            st.warning(f"Debug: Click data parse failed. Error: {e}")
    else:
        st.info("Click on the image to place the pouf.")
else:
    st.info("Please upload a room photo to get started.")
