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

st.set_page_config(page_title="Medical Image Analysis — MediScope AI", page_icon="🔬", layout="wide")

render_header()
lang = render_language_selector()

st.title("🔬 Medical Image Analysis")
st.markdown("Upload a medical radiograph or photograph, or select a sample clinical scan below for instant analysis.")

# 1. Image Upload & Selection
image, img_name, selected_modality = render_image_uploader()

if image is not None:
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image, caption=f"Selected Image: {img_name}", use_container_width=True)

    with col2:
        st.markdown("### Image Inspection & Preprocessing")
        
        # Preprocessing & Metadata Validation
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        bytes_data = img_bytes.getvalue()

        is_valid, clean_img, msg = ImagePreprocessingService.validate_and_load_image(bytes_data, img_name)
        if not is_valid:
            st.error(f"❌ Image Validation Failed: {msg}")
            st.stop()
        else:
            st.success(f"✅ {msg}")
            st.caption("🔒 Sensitive EXIF metadata stripped for patient privacy compliance.")

        # Execute Analysis Button
        if st.button("🚀 Run Specialist AI Analysis", type="primary"):
            with st.spinner("Routing image to specialist computer vision model and computing inference..."):
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
            with st.spinner("Generating structured plain-language medical educational explanation..."):
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

# Render Prediction Results if available in session state
if "active_prediction" in st.session_state and "active_explanation" in st.session_state:
    render_prediction_results(
        st.session_state.active_prediction,
        st.session_state.active_explanation,
        lang=lang
    )
