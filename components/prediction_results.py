import streamlit as st
from PIL import Image
from services.report_generator import ReportGenerator
from services.speech_service import SpeechService

def render_prediction_results(prediction, explanation_data, lang: str = "en"):
    """
    Renders prediction cards, confidence meters, visual explanations, 
    Gemini plain-language breakdown, audio playback, and report export options.
    """
    st.markdown("---")
    st.markdown("### 🔍 Analysis Results & Specialist Output")

    col_img, col_metrics = st.columns([1, 1])

    with col_img:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Visual Explanation Overlay")
        if prediction.visual_explanation_image is not None:
            st.image(
                prediction.visual_explanation_image,
                caption=f"Visual Explanation ({prediction.visual_explanation_type.upper()})",
                use_container_width=True
            )
            if prediction.visual_explanation_type == "gradcam":
                st.caption("🔥 Heatmap indicates regions of highest model attention/attribution.")
            elif prediction.visual_explanation_type == "bounding_box":
                st.caption("🔴 Bounding box highlights localized region of abnormality.")
        else:
            st.info("No visual overlay generated for this modality.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_metrics:
        status_pill = '<span class="pill-item pill-green">🟢 Active Neural Specialist</span>'
        conf_pct = float(prediction.confidence * 100)

        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <h3 style="margin: 0; color: #38bdf8;">Model Findings</h3>
                {status_pill}
            </div>
            <div style="font-size: 1rem; color: #cbd5e1; line-height: 1.7;">
                <div>🔬 <strong>Specialist Model:</strong> {prediction.specialist_name}</div>
                <div>📷 <strong>Target Modality:</strong> {prediction.modality}</div>
                <div>🏷️ <strong>Predicted Finding:</strong> <span style="font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.15); padding: 3px 10px; border-radius: 6px;">{prediction.predicted_label}</span></div>
                <div style="margin-top: 10px;">📊 <strong>Confidence Score:</strong> <span style="font-weight: 700; color: #34d399;">{conf_pct:.1f}%</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(1.0, max(0.0, float(prediction.confidence))))

        if prediction.uncertainty_note:
            st.info(f"ℹ️ **Uncertainty Note:** {prediction.uncertainty_note}")

        if prediction.all_class_probabilities:
            with st.expander("📊 Full Class Probability Distribution"):
                for label, prob in prediction.all_class_probabilities.items():
                    st.write(f"- {label}: **{prob*100:.1f}%**")

    # Structured Gemini Explanation
    st.markdown("### 📖 Educational Breakdown & Guidance")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div style="margin-bottom: 12px;">💡 <strong style="color: #38bdf8;">Summary:</strong> <span style="color: #f8fafc;">{explanation_data.get('summary', 'N/A')}</span></div>
            <div style="margin-bottom: 12px;">🔍 <strong style="color: #818cf8;">Plain Language Meaning:</strong> <span style="color: #cbd5e1;">{explanation_data.get('plain_meaning', 'N/A')}</span></div>
            <div style="margin-bottom: 12px;">⚠️ <strong style="color: #fb7185;">Limitations & Uncertainty:</strong> <span style="color: #cbd5e1;">{explanation_data.get('uncertainty_and_limitations', 'N/A')}</span></div>
            <div>⏱️ <strong style="color: #34d399;">Recommended Timeframe:</strong> <span class="pill-item pill-green" style="display: inline-block;">{explanation_data.get('urgency_guidance', 'N/A')}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #c084fc; margin-top: 0;">👨‍⚕️ Questions for Your Doctor</h4>
            <ul style="color: #cbd5e1; font-size: 0.9rem; padding-left: 18px; line-height: 1.6;">
        """, unsafe_allow_html=True)
        for q in explanation_data.get('questions_for_doctor', []):
            st.markdown(f"<li>{q}</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)

    # Audio Playback
    st.markdown("### 🔊 Spoken Response (Voice Accessibility)")
    summary_text = explanation_data.get("summary", "")
    audio_bytes = SpeechService.text_to_speech(summary_text, lang)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3")

    # Downloadable Reports
    st.markdown("---")
    st.markdown("### 📥 Export Session Report")
    
    pred_dict = {
        "specialist_name": prediction.specialist_name,
        "modality": prediction.modality,
        "task_type": prediction.task_type,
        "predicted_label": prediction.predicted_label,
        "confidence": prediction.confidence,
        "all_class_probabilities": prediction.all_class_probabilities,
        "is_demo": prediction.is_demo
    }

    md_report = ReportGenerator.generate_markdown_report(pred_dict, explanation_data)
    json_report = ReportGenerator.generate_json_report(pred_dict, explanation_data)

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "📄 Download Report (.md)",
            data=md_report,
            file_name="mediscope_analysis_report.md",
            mime="text/markdown"
        )
    with c2:
        st.download_button(
            "📊 Download Raw Data (.json)",
            data=json_report,
            file_name="mediscope_analysis_report.json",
            mime="application/json"
        )
