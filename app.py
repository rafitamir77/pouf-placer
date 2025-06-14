import streamlit as st
from PIL import Image
import numpy as np
import io
import base64
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(layout="wide")
st.title("🛋️ Try a Pouf in Your Room!")

pouf_image = Image.open("assets/pouf1.png").convert("RGBA")

uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    room_image = Image.open(uploaded_file).convert("RGBA")
    display_width = 900
    aspect_ratio = room_image.height / room_image.width
    display_height = int(display_width * aspect_ratio)
    resized = room_image.resize((display_width, display_height))

    # Convert to base64
    buffer = io.BytesIO()
    resized.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    # Sidebar
    st.sidebar.header("🪑 Adjust Pouf")
    scale = st.sidebar.slider("Scale %", 20, 500, 100)

    # JS click handler
    st.markdown(f"""
    <style>
    #clickable-img {{
        cursor: crosshair;
    }}
    </style>
    <img id="clickable-img" src="data:image/png;base64,{img_str}" width="{display_width}"/>
    """, unsafe_allow_html=True)

    coords = streamlit_js_eval(js_expressions="await (function() {{
        return new Promise(resolve => {{
            const img = window.document.getElementById('clickable-img');
            img.onclick = (e) => {{
                const rect = img.getBoundingClientRect();
                resolve({{
                    x: Math.round(e.clientX - rect.left),
                    y: Math.round(e.clientY - rect.top),
                    width: img.width,
                    height: img.height
                }});
            }};
        }});
    }})()", key="click_coords")

    if coords:
        st.success(f"Clicked at: ({coords['x']}, {coords['y']})")

        # Map click to original
        scale_x = room_image.width / coords["width"]
        scale_y = room_image.height / coords["height"]
        x_pos = int(coords["x"] * scale_x)
        y_pos = int(coords["y"] * scale_y)

        new_size = (int(pouf_image.width * scale / 100), int(pouf_image.height * scale / 100))
        scaled_pouf = pouf_image.resize(new_size)

        overlay = Image.new("RGBA", room_image.size, (255, 255, 255, 0))
        overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)
        result = Image.alpha_composite(room_image, overlay)

        st.image(result, caption="Your Room with Pouf", use_column_width=True)

        buf = io.BytesIO()
        result.save(buf, format="PNG")
        st.download_button("📥 Download Image", buf.getvalue(), "room_with_pouf.png", "image/png")
