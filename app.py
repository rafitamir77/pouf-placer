import streamlit as st
from PIL import Image, ImageOps , ImageFilter , ImageDraw
import numpy as np
import io
from streamlit_drawable_canvas import st_canvas

Pouf_Ratio = 0.25
max_display_width = 500
rerun=False
#st.write(f'xxx {xxx}.')
pouf_options = {
    "Beige Peacock": "assets/pouf1.png",
    "Red Peacock": "assets/pouf2.png",
    "Blue Peacock": "assets/pouf3.png"
}    
defaults = {
    "x_scaled": 0,
    "y_scaled": 0,
    "last_scale": 0,
    "selected_pouf": list(pouf_options.keys())[0]
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)
st.set_page_config(layout="wide") 
st.title("🛋️ Try a Pouf in Your Room!!!")  
# Upload room photo
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Fix orientation and convert to RGBA
    room_image = ImageOps.exif_transpose(Image.open(uploaded_file)).convert("RGBA")

    # Resize for canvas display
    aspect_ratio = room_image.height / room_image.width
    display_width = min(room_image.width, max_display_width)
    display_height = int(display_width * aspect_ratio)
    resized_room = room_image.resize((display_width, display_height))

    if "last_image" in st.session_state:
        # Show latest image with pouf
        canvas_rgb = st.session_state["last_image"]
    else:
        canvas_rgb = resized_room.convert("RGB") 
   


    # Sidebar controls
    # Sidebar controls
    # Sidebar controls
    # Sidebar controls
    # Sidebar controls
    # Sidebar controls
    # Sidebar controls
    st.sidebar.header("🪑 Adjust Pouf")
    scale= st.sidebar.slider(
        "Scale %",
        min_value=10,
        max_value=500,
        step=2,
        value=100
    )
    if scale != st.session_state["last_scale"]:
        rerun=True
        st.session_state["last_scale"]=scale

    st.sidebar.header("🪞 Shadow Offset (for debug)")
    light_offset_x = st.sidebar.slider("Shadow X Offset", -100, 100, 10)
    light_offset_y = st.sidebar.slider("Shadow Y Offset", -100, 100, 5)
    light_blur     = st.sidebar.slider("Blur", -10, 100, 5)
    shadow_int     = st.sidebar.slider("Shadow", -300, 300, 220)
    pouf_opacity = st.sidebar.slider("Pouf Opacity", 0, 255, 255)
    #selected_pouf = st.sidebar.selectbox("Choose Pouf Design", list(pouf_options.keys()))

    st.sidebar.header("🪑 Select a Pouf")
    cols = st.columns(len(pouf_options))
    selected_pouf = st.session_state.get("selected_pouf", list(pouf_options.keys())[0])
    for i, (label, path) in enumerate(pouf_options.items()):
        with cols[i]:
            st.sidebar.image(path, width=150)
            if st.sidebar.button(label):
                selected_pouf = label
    if selected_pouf != st.session_state["selected_pouf"]:
        rerun=True
        st.session_state["selected_pouf"]=selected_pouf   
    #st.write(f'selected_pouf {selected_pouf}.')

    pouf_image = Image.open(pouf_options[selected_pouf])

    st.sidebar.success(f"✅ selected: {selected_pouf}")


    # Canvas

    st.info("🖱️ Click on the image below to place your pouf.")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=1,
        stroke_color="white",
        background_image=canvas_rgb,
        update_streamlit=True,
        height=display_height,
        width=display_width,
        drawing_mode="point",
        display_toolbar=False,
        #key="canvas"
        key=st.session_state.get("canvas_key", "canvas")
    )
    
    # If user clicked
    if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
        #st.write("📍 Clicked at:", canvas_result.json_data["objects"][-1])
        last_click = canvas_result.json_data["objects"][-1]
        x_scaled = int(last_click["left"])
        y_scaled = int(last_click["top"])
        if x_scaled != st.session_state["x_scaled"] or \
            y_scaled != st.session_state["y_scaled"]:
            
            st.session_state["x_scaled"] = x_scaled
            st.session_state["y_scaled"] = y_scaled
            rerun = True

        # Map click to original image
        new_size = (int(display_width *Pouf_Ratio* scale / 100), int(display_height *Pouf_Ratio* scale / 100))
 
 
        scale_x = room_image.width / display_width
        scale_y = room_image.height / display_height
        x_pos = int(x_scaled - new_size[0] / 2)
        y_pos = int(y_scaled - new_size[1] / 2)



        # Resize pouf
        scaled_pouf = pouf_image.resize(new_size)
        scaled_pouf = scaled_pouf.convert("RGBA")

        # Split channels
        r, g, b, a = scaled_pouf.split()

        # Apply new alpha
        new_alpha = a.point(lambda p: int(pouf_opacity * (p / 255)))
        scaled_pouf.putalpha(new_alpha)

        # Place pouf
        overlay = Image.new("RGBA", resized_room.size, (255, 255, 255, 0))
        # Create elliptical shadow
        pouf_width, pouf_height = new_size
        
        
        shadow_size = (int(pouf_width * 0.9), int(pouf_height * 0.3))
        ellipse = Image.new("RGBA", shadow_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(ellipse)
        draw.ellipse((0, 0, *shadow_size), fill=(45, 30, 15, shadow_int))  # darker fill

        # Blur the ellipse
        blurred_shadow = ellipse.filter(ImageFilter.GaussianBlur(light_blur))
        # Resize for realism

        shadow_x = x_pos + int((pouf_width - shadow_size[0]) / 2) + light_offset_x
        shadow_y = y_pos + int(pouf_height * 0.75) + light_offset_y
        overlay.paste(blurred_shadow, (shadow_x, shadow_y),blurred_shadow     )
        overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)

        result = Image.alpha_composite(resized_room, overlay)

        # Show result
        #st.markdown("### 🖼️ Result Preview:")
        #st.image(result, use_column_width=True)
        st.session_state["last_image"] = result
        st.markdown("### 🖼️ a Preview:")   
        st.write(f'x_pos {x_pos}.')
        st.write(f'y_pos {y_pos}.')
        st.write(f'scale_x {scale_x}.')
        st.write(f'scale_y {scale_y}.')
        st.write(f'x_scaled {x_scaled}.')
        st.write(f'y_scaled {y_scaled}.')
        st.write(f'pouf_width {pouf_width}.')
        st.write(f'pouf_height {pouf_height}.')
        st.markdown("### 🕳️ Shadow Preview")


        if rerun:
            st.experimental_rerun()

        # Download
        buf = io.BytesIO()  
        result.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button("📥 Download Image", byte_im, "your_room_with_pouf.png", "image/png")
