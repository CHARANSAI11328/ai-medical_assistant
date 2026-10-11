import streamlit as st
from components.header import render_header
from components.language_controls import render_language_selector
from components.chatbot import render_chatbot

st.set_page_config(
    page_title="AI Medical Assistant — MediScope AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_header()
lang = render_language_selector()

st.markdown("""
<div style="margin-bottom: 20px;">
    <h2 style="margin: 0; color: #ffffff; font-weight: 800; letter-spacing: -0.02em;">💬 AI Medical Assistant & Conversational Triage</h2>
    <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
        Inquire about medical scan findings, explore differential health concepts, or screen acute symptoms.
    </div>
</div>
""", unsafe_allow_html=True)

# Pass current prediction if available in session
current_pred = None
if "active_prediction" in st.session_state:
    pred = st.session_state.active_prediction
    current_pred = {
        "specialist_name": pred.specialist_name,
        "predicted_label": pred.predicted_label,
        "confidence": pred.confidence
    }

render_chatbot(current_prediction=current_pred, lang=lang)
