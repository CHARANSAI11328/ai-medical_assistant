import streamlit as st
from components.header import render_header
from components.language_controls import render_language_selector
from models.registry import ModelRegistry
from PIL import Image, ImageDraw
import io

st.set_page_config(
    page_title="Agriculture AI Specialist — MediScope AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_header()
lang = render_language_selector()

st.markdown("""
<div style="margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2 style="margin: 0; color: #ffffff; font-weight: 800; letter-spacing: -0.02em;">🌿 Foliar Pathology & Crop Disease AI</h2>
        <span class="pill-item pill-green">Agronomic Specialist Active</span>
    </div>
    <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
        Modular plant pathology evaluation. <em>Dedicated agricultural extension domain partitioned from human clinical advice.</em>
    </div>
</div>
""", unsafe_allow_html=True)

col_upload, col_demo = st.columns([13, 8])

with col_upload:
    uploaded_file = st.file_uploader("Upload Crop / Leaf Photo (JPG, PNG)", type=["jpg", "jpeg", "png"])

with col_demo:
    st.markdown("""
    <div class="glass-card" style="padding: 16px;">
        <div style="color: #34d399; font-weight: 700; font-size: 0.88rem; margin-bottom: 8px;">🌱 Instant Benchmark Foliar Scan</div>
        <div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 12px;">Load verified sample of Apple / Corn leaf with foliar rust lesions.</div>
    """, unsafe_allow_html=True)
    if st.button("🌱 Load Synthetic Rust Leaf Sample", use_container_width=True):
        img_leaf = Image.new("RGB", (300, 300), color=(235, 240, 245))
        draw = ImageDraw.Draw(img_leaf)
        draw.ellipse([60, 40, 240, 260], fill=(35, 150, 48), outline=(18, 80, 26), width=3)
        draw.ellipse([100, 100, 150, 150], fill=(155, 80, 22))  # Rust lesion spot
        st.session_state.agri_image = img_leaf
    st.markdown("</div>", unsafe_allow_html=True)

agri_img = None
if uploaded_file is not None:
    try:
        agri_img = Image.open(uploaded_file)
    except Exception as e:
        st.error(f"Error loading image: {e}")
elif "agri_image" in st.session_state:
    agri_img = st.session_state.agri_image

if agri_img is not None:
    st.markdown("""<div style="margin: 20px 0 16px 0; border-top: 1px solid rgba(255, 255, 255, 0.08);"></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""<div style="color: #34d399; font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;">📷 Foliar Image Inspection</div>""", unsafe_allow_html=True)
        st.image(agri_img, caption="Crop Foliage Input", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""<div style="color: #ffffff; font-weight: 700; font-size: 1rem; margin-bottom: 12px;">🌾 Plant Pathology Diagnostics</div>""", unsafe_allow_html=True)
        
        if st.button("🔍 Run Foliar Health Analysis", type="primary", use_container_width=True):
            registry = ModelRegistry()
            spec = registry.get_specialist("agriculture")
            if spec:
                pred = spec.predict(agri_img)

                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); 
                            border-radius: 10px; padding: 14px; margin: 14px 0;">
                    <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;">CLASSIFICATION RESULT:</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #34d399; margin: 4px 0;">{pred.predicted_label}</div>
                    <div style="font-size: 0.9rem; color: #cbd5e1;">Confidence: <strong style="color: #f8fafc;">{pred.confidence*100:.1f}%</strong></div>
                </div>
                """, unsafe_allow_html=True)

                st.progress(min(1.0, max(0.0, float(pred.confidence))))

                if pred.visual_explanation_image:
                    st.image(pred.visual_explanation_image, caption="Foliar Lesion Attention Map", use_container_width=True)

                st.markdown("""<div style="margin-top: 14px;"><strong style="color: #38bdf8;">🚜 Agronomic Guidance:</strong></div>""", unsafe_allow_html=True)
                if "Rust" in pred.predicted_label or "Blight" in pred.predicted_label:
                    st.markdown("""
                    <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; border-radius: 8px; padding: 12px; margin-top: 8px; color: #fef3c7; font-size: 0.88rem; line-height: 1.6;">
                        <div>1. <strong>Field Quarantine:</strong> Isolate affected crop acreage to prevent aerial spore transmission.</div>
                        <div>2. <strong>Canopy Aeration:</strong> Ensure adequate plant spacing and avoid overhead evening watering.</div>
                        <div>3. <strong>Extension Verification:</strong> Consult local agricultural extension specialists for certified antifungal treatments.</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; border-radius: 8px; padding: 12px; margin-top: 8px; color: #d1fae5; font-size: 0.88rem;">
                        Leaf foliage shows zero pathogenic lesions. Continue standard drip irrigation and soil nutrient management.
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
