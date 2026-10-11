import streamlit as st
import os

def render_language_selector() -> str:
    """Renders sleek sidebar brand banner, language selection widget, and Gemini API key config."""
    # Sidebar Header Brand Card
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%); 
                border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 14px 16px; margin-bottom: 18px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <span style="font-weight: 800; font-size: 1.15rem; color: #ffffff; letter-spacing: -0.02em;">🏥 MediScope AI</span>
            <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; font-size: 0.72rem; font-weight: 700; 
                         padding: 2px 8px; border-radius: 9999px; border: 1px solid rgba(16, 185, 129, 0.4);">v2.5 PRO</span>
        </div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">Clinical Intelligence & Vision Suite</div>
    </div>
    """, unsafe_allow_html=True)

    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "en"

    languages = {
        "en": "🇬🇧 English",
        "hi": "🇮🇳 Hindi (हिंदी)",
        "te": "🇮🇳 Telugu (తెలుగు)"
    }

    selected_label = st.sidebar.selectbox(
        "🌐 Choose Language / भाषा चुनें / భాష",
        options=list(languages.values()),
        index=0
    )

    for code, label in languages.items():
        if label == selected_label:
            st.session_state.selected_language = code
            break

    st.sidebar.markdown("""
    <div style="margin: 12px 0 6px 0; border-top: 1px solid rgba(255, 255, 255, 0.08);"></div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("🔑 **Google Gemini API Configuration**")
    
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
        st.sidebar.markdown("""
        <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.35); 
                    border-radius: 8px; padding: 6px 10px; font-size: 0.78rem; color: #34d399; font-weight: 600; 
                    margin-top: 4px; display: flex; align-items: center; gap: 6px;">
            <span>🟢</span> <span>Gemini API Key Active</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.2); 
                    border-radius: 8px; padding: 6px 10px; font-size: 0.76rem; color: #94a3b8; margin-top: 4px;">
            Using verified offline medical reasoning engine.
        </div>
        """, unsafe_allow_html=True)

    # Privacy badge at bottom of sidebar
    st.sidebar.markdown("""
    <div style="margin-top: 24px; padding: 10px 12px; background: rgba(15, 23, 42, 0.5); 
                border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 10px;">
        <div style="color: #94a3b8; font-size: 0.74rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">🔒 Clinical Privacy</div>
        <div style="color: #64748b; font-size: 0.72rem; margin-top: 3px; line-height: 1.4;">Zero patient metadata retained. EXIF headers stripped automatically.</div>
    </div>
    """, unsafe_allow_html=True)

    return st.session_state.selected_language
