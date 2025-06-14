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

    # Sidebar scale
    st.sidebar.header("🪑 Adjust Pouf")
    scale = st.sidebar.slider("Scale %", 20, 500, 100)

    # Capture click from JS
    click_data = st.experimental_get_query_params()
    x = int(click_data.get("x", [0])[0])
    y = int(click_data.get("y", [0])[0])
    w = int(click_data.get("width", [display_width])[0])
    h = int(click_data.get("height", [display_height])[0])

    if x > 0 and y > 0:
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

    # Inject custom HTML + JS to capture click
    components.html(f"""
    <script>
      window.addEventListener('DOMContentLoaded', function() {{
        const img = document.getElementById("room_image");
        if (!img) return;

        img.style.cursor = "crosshair";
        img.addEventListener("click", function(e) {{
          const rect = img.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const query = `?x=${{x}}&y=${{y}}&width=${{img.width}}&height=${{img.height}}`;
          window.location.search = query;
        }});
      }});
    </script>
    <img id="room_image" src="data:image/png;base64,{base64_img}" width="{display_width}"/>
    """, height=display_height + 50)

else:
    st.info("Please upload a room photo to get started.")
