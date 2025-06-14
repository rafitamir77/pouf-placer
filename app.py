import streamlit as st
from PIL import Image, ImageOps , ImageFilter
import numpy as np
import io
from streamlit_drawable_canvas import st_canvas

Pouf_Ratio = 0.25
scale_key = "scale_slider"


st.set_page_config(layout="wide") 
st.title("🛋️ Try a Pouf in Your Room!")

# Load pouf image
pouf_image = Image.open("assets/pouf1.png")

# Upload room photo
uploaded_file = st.file_uploader("📷 Upload your room photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Fix orientation and convert to RGBA
    room_image = ImageOps.exif_transpose(Image.open(uploaded_file)).convert("RGBA")

    # Resize for canvas display
    max_display_width = 500
    aspect_ratio = room_image.height / room_image.width
    display_width = min(room_image.width, max_display_width)
    display_height = int(display_width * aspect_ratio)
    resized_room = room_image.resize((display_width, display_height))

    #st.write(f'aspect_ratio {aspect_ratio}.')

    rerun=False
    if "x_scaled" not in  st.session_state:   
        st.session_state["x_scaled"] = 0
    if "y_scaled" not in  st.session_state:   
        st.session_state["y_scaled"] = 0
    if "last_scale" not in  st.session_state:   
        st.session_state["last_scale"] = 0
    if "reset_scale" not in  st.session_state:   
        st.session_state["reset_scale"] = False
    if scale_key not in  st.session_state:   
        st.session_state[scale_key] = 100

    if "last_image" in st.session_state:
        # Show latest image with pouf
        resized_room = st.session_state["last_image"].resize((display_width, display_height))
    else:
        resized_room = resized_room;
        

    # Convert resized image to NumPy RGB array (✅ required for canvas)
    background_rgb = resized_room.convert("RGB") 
    #background_rgb = resized_room

    # Sidebar controls
    st.sidebar.header("🪑 Adjust Pouf")
    if st.session_state["reset_scale"]:
        st.session_state[scale_key] = 100
        st.session_state["reset_scale"]=False;
        
    scale = st.sidebar.slider("Scale %", 20, 500,  st.session_state[scale_key], step=3, key=scale_key)
    if st.sidebar.button("🔄 Reset Canvas"):
        if "last_image" in st.session_state:
            del st.session_state["last_image"]
        st.session_state["x_scaled"]=0 
        st.session_state["y_scaled"]=0       
        st.session_state["reset_scale"]=True       
        st.session_state["canvas_key"] = str(np.random.rand())
        st.experimental_rerun()
 
    if scale != st.session_state["last_scale"]:
        rerun=True;
        st.session_state["last_scale"]=scale

    pouf_options = {
    "Beige Peacock": "assets/pouf1.png",
    "Blue Peacock": "assets/pouf1.png",
    "Red Peacock": "assets/pouf1.png"
}
    selected_pouf = st.sidebar.selectbox("Choose Pouf Design", list(pouf_options.keys()))
    pouf_image = Image.open(pouf_options[selected_pouf])

  
    # Canvas
    st.info("🖱️ Click on the image below to place your pouf.")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=1,
        stroke_color="white",
        background_image=background_rgb,
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
        x_pos = int(x_scaled * scale_x - new_size[0] / 2)
        y_pos = int(y_scaled * scale_y - new_size[1] / 2)


        # Resize pouf
        scaled_pouf = pouf_image.resize(new_size)

        # Place pouf
        overlay = Image.new("RGBA", room_image.size, (255, 255, 255, 0))
        overlay.paste(scaled_pouf, (x_pos, y_pos), mask=scaled_pouf)
        shadow = Image.new("RGBA", scaled_pouf.size, (0, 0, 0, 80))
        blurred_shadow = shadow.filter(ImageFilter.GaussianBlur(8))
        overlay.paste(blurred_shadow, (x_pos+5, y_pos+5), blurred_shadow)

        result = Image.alpha_composite(room_image, overlay)

        # Show result
        #st.markdown("### 🖼️ Result Preview:")
        #st.image(result, use_column_width=True)
        st.session_state["last_image"] = result

        if rerun:
            st.experimental_rerun()

        # Download
        buf = io.BytesIO()  
        result.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button("📥 Download Image", byte_im, "your_room_with_pouf.png", "image/png")
