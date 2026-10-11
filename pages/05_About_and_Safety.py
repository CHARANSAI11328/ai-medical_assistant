import streamlit as st
from components.header import render_header
from components.language_controls import render_language_selector
from services.session_service import SessionService

st.set_page_config(
    page_title="About, Privacy & Safety — MediScope AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_header()
lang = render_language_selector()

st.markdown("""
<div style="margin-bottom: 20px;">
    <h2 style="margin: 0; color: #ffffff; font-weight: 800; letter-spacing: -0.02em;">🛡️ Clinical Governance, Privacy & Safety Protocols</h2>
    <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
        Institutional AI research disclaimers, GDPR/HIPAA-aligned privacy mechanisms, and emergency care directives.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="glass-card" style="border-top: 3px solid #38bdf8;">
        <h4 style="color: #38bdf8; margin: 0 0 10px 0;">🏥 Platform Mission & Architecture Scope</h4>
        <p style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.7;">
            <strong>MediScope AI</strong> is an advanced clinical AI research prototype engineered to showcase multi-specialist vision routing, Grad-CAM attention attribution, YOLOv8 bounding box localization, and conversational medical triage powered by Google Gemini 3.5.
        </p>
    </div>

    <div class="glass-card" style="border-top: 3px solid #10b981;">
        <h4 style="color: #34d399; margin: 0 0 10px 0;">🔒 Data Protection & Zero Retention Policy</h4>
        <ul style="color: #cbd5e1; font-size: 0.88rem; padding-left: 18px; line-height: 1.7; margin-bottom: 0;">
            <li><strong>Automated EXIF Stripping:</strong> Uploaded images have all device, patient identity, and geographical tags scrubbed in memory prior to analysis.</li>
            <li><strong>Volatile Memory Only:</strong> Imaging buffers exist solely in transient RAM and are never permanently persisted to disk or external cloud stores.</li>
            <li><strong>Decoupled Telemetry:</strong> All diagnostic logging is pseudonymous and decoupled from client identity.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card" style="border-top: 3px solid #ef4444; border-left: 4px solid #ef4444;">
        <h4 style="color: #fca5a5; margin: 0 0 10px 0;">⚠️ Mandatory Medical Disclaimers</h4>
        <ol style="color: #cbd5e1; font-size: 0.88rem; padding-left: 18px; line-height: 1.7; margin-bottom: 0;">
            <li><strong>Not a Certified Diagnostic Device:</strong> MediScope AI is not FDA/CE marked and cannot replace licensed clinical judgment.</li>
            <li><strong>Non-Zero Error Margin:</strong> Deep learning vision models can produce false positives and false negatives. A negative finding does not exclude disease.</li>
            <li><strong>Emergency Care Directive:</strong> For acute symptoms (chest pain, stroke signs, severe dyspnea, sudden blindness), <strong>call emergency services immediately</strong>:
                <div style="background: rgba(239, 68, 68, 0.15); padding: 8px 12px; border-radius: 8px; margin-top: 6px; font-weight: 700; color: #fecaca;">
                    📞 US: 911 &nbsp;|&nbsp; 📞 Europe: 112 &nbsp;|&nbsp; 📞 India: 108 / 102
                </div>
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="border-top: 3px solid #f59e0b;">
        <h4 style="color: #fbbf24; margin: 0 0 10px 0;">🧹 Volatile Session Purge (Privacy Control)</h4>
        <div style="color: #94a3b8; font-size: 0.82rem; margin-bottom: 12px;">
            Purge all cached scan tensors, differential history, and conversational memory from the local session.
        </div>
    """, unsafe_allow_html=True)
    if st.button("🗑️ Purge All Session Tensors & Reset Memory", type="primary", use_container_width=True):
        session_svc = SessionService()
        session_svc.clear_session_data()
        st.session_state.clear()
        st.success("✅ All session tensors, cached predictions, and chat context have been purged.")
    st.markdown("</div>", unsafe_allow_html=True)
