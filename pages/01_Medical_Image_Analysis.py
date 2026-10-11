import streamlit as st
from components.header import render_header
from components.language_controls import render_language_selector
from components.image_uploader import render_image_uploader
from components.prediction_results import render_prediction_results
from services.image_preprocessing import ImagePreprocessingService
from models.router import SpecialistRouter
from services.gemini_service import GeminiMedicalService
from services.session_service import SessionService
import io

st.set_page_config(
    page_title="Medical Image Analysis — MediScope AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_header()
lang = render_language_selector()

st.markdown("""
<div style="margin-bottom: 20px;">
    <h2 style="margin: 0; color: #ffffff; font-weight: 800; letter-spacing: -0.02em;">🔬 Specialist Computer Vision & Image Analysis</h2>
    <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
        High-precision neural computer vision routing across Retinal, Pulmonary, and Skeletal modalities.
    </div>
</div>
""", unsafe_allow_html=True)

# 1. Image Upload & Selection
image, img_name, selected_modality = render_image_uploader()

if image is not None:
    st.markdown("""<div style="margin: 20px 0 16px 0; border-top: 1px solid rgba(255, 255, 255, 0.08);"></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #38bdf8; font-size: 0.92rem;">📷 Raw Scan Preview</strong>
            <span class="pill-item">{img_name}</span>
        </div>
        """, unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <strong style="color: #ffffff; font-size: 1rem;">🔒 Image Preprocessing & Ingestion Shield</strong>
            <span class="pill-item pill-green">GDPR/HIPAA Ready</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Preprocessing & Metadata Validation
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        bytes_data = img_bytes.getvalue()

        is_valid, clean_img, msg = ImagePreprocessingService.validate_and_load_image(bytes_data, img_name)
        if not is_valid:
            st.error(f"❌ Image Validation Failed: {msg}")
            st.stop()
        else:
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); 
                        border-radius: 10px; padding: 10px 14px; color: #34d399; font-size: 0.88rem; margin-bottom: 12px;">
                ✅ <strong>Validation Passed:</strong> {msg}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="color: #94a3b8; font-size: 0.82rem; line-height: 1.6; margin-bottom: 16px;">
                <div>🛡️ <strong>Metadata Privacy:</strong> Sensitive EXIF / patient headers stripped in volatile memory.</div>
                <div>📐 <strong>Tensor Geometry:</strong> Standardized 224x224 RGB normalization applied.</div>
                <div>🎯 <strong>Selected Routing Target:</strong> <code style="color: #38bdf8;">{}</code></div>
            </div>
            """.format(selected_modality.upper()), unsafe_allow_html=True)

        # Execute Analysis Button
        if st.button("🚀 Run Specialist AI Analysis", type="primary", use_container_width=True):
            with st.spinner("Routing image to specialist neural architecture and computing inference..."):
                router = SpecialistRouter()
                route_success, specialist_model, route_msg = router.route_image(clean_img, selected_modality)

                if not route_success or specialist_model is None:
                    st.error(f"❌ Routing Error: {route_msg}")
                    st.stop()

                # Model Prediction
                prediction = specialist_model.predict(clean_img)

                # Store active prediction in session state
                st.session_state.active_prediction = prediction

            # Gemini Plain-Language Explanation
            with st.spinner("Generating structured clinical breakdown via Gemini 3.5..."):
                gemini_service = GeminiMedicalService()
                explanation_data = gemini_service.generate_prediction_explanation(
                    specialist_name=prediction.specialist_name,
                    modality=prediction.modality,
                    predicted_label=prediction.predicted_label,
                    confidence=prediction.confidence,
                    uncertainty_note=prediction.uncertainty_note,
                    lang=lang
                )
                st.session_state.active_explanation = explanation_data

            # Record Session History
            session_svc = SessionService()
            session_svc.record_analysis_session(img_name, specialist_model.key, {
                "predicted_label": prediction.predicted_label,
                "confidence": prediction.confidence,
                "is_demo": prediction.is_demo
            })
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# Render Prediction Results if available in session state
if "active_prediction" in st.session_state and "active_explanation" in st.session_state:
    render_prediction_results(
        st.session_state.active_prediction,
        st.session_state.active_explanation,
        lang=lang
    )
