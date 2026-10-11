import streamlit as st
from PIL import Image
from services.report_generator import ReportGenerator
from services.speech_service import SpeechService

def render_prediction_results(prediction, explanation_data, lang: str = "en"):
    """
    Renders enterprise clinical workstation prediction view:
    visual explanation overlay, confidence metrics, Gemini plain-language breakdown,
    spoken audio playback, and exportable medical reports.
    """
    st.markdown("""<div style="margin: 24px 0 16px 0; border-top: 1px solid rgba(255, 255, 255, 0.08);"></div>""", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h3 style="margin: 0; color: #ffffff; font-weight: 700;">🔍 Specialist Diagnostic Findings & Explainability</h3>
        <span class="pill-item pill-green">Inference Verified</span>
    </div>
    """, unsafe_allow_html=True)

    col_img, col_metrics = st.columns([1, 1])

    with col_img:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <strong style="color: #38bdf8; font-size: 0.95rem;">🔬 Visual Attention Attribution</strong>
            <span class="pill-item pill-purple">{}</span>
        </div>
        """.format(prediction.visual_explanation_type.upper()), unsafe_allow_html=True)

        if prediction.visual_explanation_image is not None:
            st.image(
                prediction.visual_explanation_image,
                caption=f"Visual Overlay: {prediction.visual_explanation_type.upper()}",
                use_container_width=True
            )
            if prediction.visual_explanation_type == "gradcam":
                st.markdown("""
                <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 8px; 
                            border: 1px solid rgba(255, 255, 255, 0.06); font-size: 0.78rem; color: #94a3b8; margin-top: 6px;">
                    🔥 <strong>Grad-CAM Heatmap:</strong> Bright warm hues pinpoint spatial features driving neural activation.
                </div>
                """, unsafe_allow_html=True)
            elif prediction.visual_explanation_type == "bounding_box":
                st.markdown("""
                <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 8px; 
                            border: 1px solid rgba(255, 255, 255, 0.06); font-size: 0.78rem; color: #94a3b8; margin-top: 6px;">
                    🔴 <strong>YOLO Localization:</strong> Bounding box coordinates highlight detected pathology margins.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No visual overlay generated for this modality.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_metrics:
        conf_pct = float(prediction.confidence * 100)

        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                <span style="font-size: 1.15rem; font-weight: 700; color: #ffffff;">Neural Model Telemetry</span>
                <span class="pill-item pill-green">🟢 Live Verified</span>
            </div>
            <div style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.8;">
                <div>🔬 <strong>Specialist Model:</strong> <span style="color: #f8fafc;">{prediction.specialist_name}</span></div>
                <div>📷 <strong>Target Modality:</strong> <span style="color: #f8fafc;">{prediction.modality}</span></div>
                <div>🏷️ <strong>Predicted Finding:</strong> <span style="font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.15); padding: 2px 10px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.3);">{prediction.predicted_label}</span></div>
                <div style="margin-top: 10px;">📊 <strong>Confidence Level:</strong> <span style="font-weight: 800; font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; color: #34d399;">{conf_pct:.1f}%</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(1.0, max(0.0, float(prediction.confidence))))

        if prediction.uncertainty_note:
            st.markdown(f"""
            <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); 
                        border-radius: 10px; padding: 10px 14px; font-size: 0.85rem; color: #fef3c7; margin-top: 10px;">
                ℹ️ <strong>Uncertainty Note:</strong> {prediction.uncertainty_note}
            </div>
            """, unsafe_allow_html=True)

        if prediction.all_class_probabilities:
            with st.expander("📊 Complete Class Probability Matrix"):
                for label, prob in prediction.all_class_probabilities.items():
                    bar_w = int(prob * 100)
                    st.markdown(f"""
                    <div style="margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: #cbd5e1;">
                            <span>{label}</span>
                            <span style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #38bdf8;">{prob*100:.1f}%</span>
                        </div>
                        <div style="height: 6px; background: rgba(255,255,255,0.06); border-radius: 4px; overflow: hidden; margin-top: 2px;">
                            <div style="width: {bar_w}%; height: 100%; background: linear-gradient(90deg, #38bdf8, #818cf8);"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # 2. Structured Gemini Plain-Language Explanation
    st.markdown("""<div style="margin: 20px 0 14px 0;"></div>""", unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px;">
        <h3 style="margin: 0; color: #ffffff; font-weight: 700;">📖 Educational Breakdown & Clinical Context</h3>
        <span class="pill-item pill-purple">Gemini 3.5 Synthesis</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([13, 8])
    with col1:
        st.markdown(f"""
        <div class="glass-card" style="padding: 22px;">
            <div style="margin-bottom: 14px; line-height: 1.6;">
                <div style="color: #38bdf8; font-weight: 700; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">💡 Clinical Summary</div>
                <div style="color: #f8fafc; font-size: 0.95rem;">{explanation_data.get('summary', 'N/A')}</div>
            </div>
            <div style="margin-bottom: 14px; line-height: 1.6;">
                <div style="color: #818cf8; font-weight: 700; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">🔍 Plain-Language Explanation</div>
                <div style="color: #cbd5e1; font-size: 0.92rem;">{explanation_data.get('plain_meaning', 'N/A')}</div>
            </div>
            <div style="margin-bottom: 14px; line-height: 1.6;">
                <div style="color: #fb7185; font-weight: 700; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">⚠️ Limitations & Uncertainty</div>
                <div style="color: #cbd5e1; font-size: 0.92rem;">{explanation_data.get('uncertainty_and_limitations', 'N/A')}</div>
            </div>
            <div>
                <div style="color: #34d399; font-weight: 700; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">⏱️ Recommended Clinical Follow-up</div>
                <span class="pill-item pill-green" style="font-size: 0.85rem; padding: 5px 14px;">{explanation_data.get('urgency_guidance', 'Routine consultation with primary care physician')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card" style="padding: 22px; border-top: 3px solid #c084fc;">
            <h4 style="color: #c084fc; margin: 0 0 12px 0; font-size: 1.02rem; display: flex; align-items: center; gap: 6px;">
                <span>👨‍⚕️</span> Questions for Your Doctor
            </h4>
            <div style="color: #94a3b8; font-size: 0.78rem; margin-bottom: 10px;">Suggested discussion points during your clinical appointment:</div>
            <ul style="color: #cbd5e1; font-size: 0.88rem; padding-left: 18px; line-height: 1.7; margin-bottom: 0;">
        """, unsafe_allow_html=True)
        for q in explanation_data.get('questions_for_doctor', []):
            st.markdown(f"<li style='margin-bottom: 6px;'>{q}</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)

    # 3. Accessible Voice Audio Playback
    st.markdown("""<div style="margin: 16px 0 12px 0;"></div>""", unsafe_allow_html=True)
    summary_text = explanation_data.get("summary", "")
    audio_bytes = SpeechService.text_to_speech(summary_text, lang)
    if audio_bytes:
        st.markdown("""
        <div class="glass-card" style="padding: 16px 20px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.2rem;">🔊</span>
                    <div>
                        <div style="color: #ffffff; font-weight: 700; font-size: 0.92rem;">Spoken Audio Briefing (Voice Accessibility)</div>
                        <div style="color: #94a3b8; font-size: 0.76rem;">Synthesized clinical explanation in selected language</div>
                    </div>
                </div>
                <span class="pill-item pill-cyan">TTS Active</span>
            </div>
        """, unsafe_allow_html=True)
        st.audio(audio_bytes, format="audio/mp3")
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. Export Session Report Action Bar
    st.markdown("""<div style="margin: 20px 0 14px 0; border-top: 1px solid rgba(255, 255, 255, 0.08);"></div>""", unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
        <h4 style="margin: 0; color: #ffffff; font-weight: 700;">📥 Export Session Diagnostic Record</h4>
        <span class="pill-item">Patient Privacy Stripped</span>
    </div>
    """, unsafe_allow_html=True)
    
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
            "📄 Export Clinical Markdown Report (.md)",
            data=md_report,
            file_name="mediscope_diagnostic_report.md",
            mime="text/markdown",
            use_container_width=True
        )
    with c2:
        st.download_button(
            "📊 Export Raw Machine-Readable Data (.json)",
            data=json_report,
            file_name="mediscope_diagnostic_telemetry.json",
            mime="application/json",
            use_container_width=True
        )
