import streamlit as st
import os

def render_language_selector() -> str:
    """Renders language selection widget and Gemini API key input in Streamlit sidebar."""
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "en"

    languages = {
        "en": "🇬🇧 English",
        "hi": "🇮🇳 Hindi (हिंदी)",
        "te": "🇮🇳 Telugu (తెలుగు)"
    }

    selected_label = st.sidebar.selectbox(
        "🌐 Choose Language / भाषा चुनें / భాషను ఎంచుకోండి",
        options=list(languages.values()),
        index=0
    )

    for code, label in languages.items():
        if label == selected_label:
            st.session_state.selected_language = code
            break

    st.sidebar.markdown("---")
    st.sidebar.markdown("🔑 **Google Gemini API Key Config**")
    
    current_key = os.environ.get("GEMINI_API_KEY", "")
    api_key_input = st.sidebar.text_input(
        "Paste Gemini API Key:",
        value=st.session_state.get("user_gemini_api_key", current_key),
        type="password",
        help="Paste your Google Gen AI Gemini API key here to activate live LLM medical explanations."
    )

    if api_key_input:
        st.session_state.user_gemini_api_key = api_key_input.strip()
        os.environ["GEMINI_API_KEY"] = api_key_input.strip()
        st.sidebar.success("🔑 Gemini API Key Active")
    else:
        st.sidebar.caption("Using offline baseline educational response mode.")

    return st.session_state.selected_language
