import streamlit as st
from components.header import render_header
from components.language_controls import render_language_selector
from models.registry import ModelRegistry
from PIL import Image, ImageDraw
import io

st.set_page_config(page_title="Agriculture AI Specialist — MediScope AI", page_icon="🌿", layout="wide")

render_header()
lang = render_language_selector()

st.title("🌿 Agriculture AI — Plant & Crop Disease Specialist")
st.markdown("Modular agricultural plant health evaluation. *Kept separate from human medical advice.*")

col_upload, col_demo = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader("Upload Crop / Leaf Photo (JPG, PNG)", type=["jpg", "jpeg", "png"])

with col_demo:
    st.markdown("**or Use Demo Leaf Image:**")
    if st.button("🌱 Load Demo Rust Leaf"):
        img_leaf = Image.new("RGB", (300, 300), color=(240, 240, 240))
        draw = ImageDraw.Draw(img_leaf)
        draw.ellipse([60, 40, 240, 260], fill=(40, 160, 50), outline=(20, 90, 30), width=3)
        draw.ellipse([100, 100, 150, 150], fill=(160, 90, 30))  # Rust lesion spot
        st.session_state.agri_image = img_leaf

agri_img = None
if uploaded_file is not None:
    try:
        agri_img = Image.open(uploaded_file)
    except Exception as e:
        st.error(f"Error loading image: {e}")
elif "agri_image" in st.session_state:
    agri_img = st.session_state.agri_image

if agri_img is not None:
    st.markdown("---")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.image(agri_img, caption="Crop Leaf Input", use_container_width=True)

    with c2:
        if st.button("🔍 Run Plant Health Analysis", type="primary"):
            registry = ModelRegistry()
            spec = registry.get_specialist("agriculture")
            if spec:
                pred = spec.predict(agri_img)

                st.subheader("🌾 Crop Disease Findings")
                st.markdown(f"**Predicted Status:** `{pred.predicted_label}`")
                st.markdown(f"**Confidence:** {pred.confidence*100:.1f}%")
                st.progress(min(1.0, max(0.0, float(pred.confidence))))

                if pred.visual_explanation_image:
                    st.image(pred.visual_explanation_image, caption="Foliar Lesion Heatmap", use_container_width=True)

                st.markdown("### 🚜 Agronomic Recommendations")
                if "Rust" in pred.predicted_label or "Blight" in pred.predicted_label:
                    st.warning(
                        "1. **Isolation:** Isolate affected crop area to prevent fungal spore transmission.\n"
                        "2. **Air Circulation:** Ensure adequate row spacing and avoid overhead evening watering.\n"
                        "3. **Expert Agronomist Review:** Consult local agricultural extension services for organic/approved treatment protocols."
                    )
                else:
                    st.success("Leaf foliage appears healthy. Continue standard crop irrigation and nutrient monitoring.")
