# 🛋️ Pouf Placer App

**Try Mandala Life Art Poufs in Your Room — using AI!**

Upload a photo of your room and place one of our beautiful Mandala Life Art poufs using a smart AI model that detects your floor automatically. No downloads, no design skills needed — just see how our boho poufs would look in your own space.

---

## ✨ Demo

🟢 [Click here to try it on Streamlit](https://pouf-placer-gszdz8qf3jmxuk3xaly2ei.streamlit.app/)

> *(replace with your real Streamlit app link)*

---

## 📸 How It Works

- 🖼 Upload a photo of your room
- 🤖 AI detects the floor using MiDaS depth estimation
- 🪑 Our pouf is placed naturally in your space
- 🧡 Download and share your personalized room render

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/) for web app UI
- [OpenCV](https://opencv.org/) for image processing
- [Pillow](https://python-pillow.org/) for image manipulation
- [MiDaS](https://github.com/isl-org/MiDaS) for depth estimation
- Python (with NumPy & Torch)

---

## 📦 Installation (Local Development)

```bash
git clone https://github.com/rafitamir77/pouf-placer.git
cd pouf-placer
pip install -r requirements.txt
streamlit run app.py  

uploaded_file
aspect_ratio = room_image.height / room_image.width
display_width = min(room_image.width, max_display_width)
display_height = int(display_width * aspect_ratio)
pouf_image = Image.open(pouf_options[selected_pouf])
scaled_pouf = pouf_image.resize(new_size)
x_pos = int(x_scaled - new_size[0] / 2)
y_pos = int(y_scaled - new_size[1] / 2)



st.session_state["resized_room"]    resized_room
st.session_state["last_image"]
st.session_state["last_scale"]      scale
st.session_state["selected_pouf"]   selected_pouf 
st.session_state["x_scaled"] 		x_scaled - click position
st.session_state["y_scaled"] 		y_scaled - click position
st.session_state[""]   
st.session_state[""]   
st.session_state[""]   
