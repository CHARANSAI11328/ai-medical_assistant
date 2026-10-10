import streamlit as st
from components.header import render_header
from components.language_controls import render_language_selector
from components.chatbot import render_chatbot

st.set_page_config(page_title="AI Medical Assistant — MediScope AI", page_icon="💬", layout="wide")

render_header()
lang = render_language_selector()

st.title("💬 AI Medical Assistant & Conversational Triage")
st.markdown("Ask health-related questions, inquire about medical scan findings, or discuss general symptoms.")

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
