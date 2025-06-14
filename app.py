import streamlit as st
from PIL import Image
import io
import base64
import numpy as np
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(layout="wide")
st.title("🛋️ Try a Pouf in Your Room!")

# Load pouf image
pouf_image = Image.open("assets/pouf1.png").convert("RGBA")

# Upload room photo
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "jpeg", "png"])

# Sidebar scale
st.sidebar.header("🪑 Adjust Pouf")
scale = st.sidebar.slider("Scale %", 20, 500, 100)

if uploaded_file:
    room_image = Image.open(uploaded_file).convert("RGBA")
    display_width = 900
    aspect_ratio = room_image.height / room_image.width
    display_height = int(display_width * aspect_ratio)
    resized_image = room_image.resize((display_width, display_height))

    # Convert to base64 for JS rendering
    buffered = io.BytesIO()
    resized_image.save(buffered, format="PNG")
    base64_img = base64.b64encode(buffered.getvalue()).decode()

    # Display image with JS click listener
    st.markdown(f"""
        <img id="room_image_custom" src="data:image/png;base64,{base64_img}"
             width="{display_width}" height="{display_height}" style="cursor:crosshair;" />
    """, unsafe_allow_html=True)

    # Capture click coordinates from JavaScript
    coords = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve) => {
            const img = document.getElementById("room_image_custom");
            if (img) {
                img.onclick = function (e) {
                    const rect = img.getBoundingClientRect();
                    const x = Math.round(e.clientX - rect.left);
                    const y = Math.round(e.clientY - rect.top);
                    resolve({x: x, y: y, width: img.width, height: img.height});
                };
            } else {
                resolve(null);
            }
        });
        """,
        key="click_coords"
    )

    if coords and "x" in coords:
        st.success(f"Clicked at ({coords['x']}, {coords['y']})")

        # Map to original image
        scale_x = room_image.width / coords["width"]
        scale_y = room_image.height / coords["height"]
        x_pos = int(coords["x"] * scale_x)
        y_pos = int(coords["y"] * scale_y)

        # Resize pouf
        new_size = (int(pouf_image.width * scale / 100), int(pouf_image.height * scale / 100))
        scaled_pouf = pouf_image.resize(new_size)

        # Create result image
        overlay = Image.new("RGBA", room_image.size, (255, 255, 255, 0))
        overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)
        result = Image.alpha_composite(room_image, overlay)

        st.image(result, caption="🖼️ Your Room with Pouf", use_column_width=True)

        # Download button
        buf = io.BytesIO()
        result.save(buf, format="PNG")
        st.download_button("📥 Download Image", buf.getvalue(), "your_room_with_pouf.png", "image/png")

    else:
        st.info("🖱️ Click on the image to place your pouf.")

else:
    st.info("📤 Please upload a room photo to begin.")
