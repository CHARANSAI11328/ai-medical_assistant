import streamlit as st
from services.medical_assistant import MedicalAssistantOrchestrator
from services.speech_service import SpeechService
from services.gemini_service import GeminiMedicalService

def render_chatbot(current_prediction=None, lang: str = "en"):
    """
    Renders interactive medical conversational assistant chat UI.
    """
    c_title, c_status, c_reset = st.columns([3, 2, 1])
    with c_title:
        st.markdown("### 💬 AI Medical Assistant Chat")
    with c_status:
        gemini_svc = GeminiMedicalService()
        if gemini_svc.is_available and gemini_svc.api_key:
            st.success("🟢 Gemini API Live & Connected")
        else:
            st.info("🟡 Offline / Demo Mode Active")
    with c_reset:
        if st.button("🔄 Clear Chat", key="clear_chat_btn"):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Hello! I am your MediScope AI Medical Information Assistant. How can I help you with medical concepts, symptoms, or scan results today?"}
            ]
            st.rerun()
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! I am your MediScope AI Medical Information Assistant. How can I help you with medical concepts, symptoms, or scan results today?"}
        ]

    orchestrator = MedicalAssistantOrchestrator()

    # Render previous messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input Box
    user_input = st.chat_input("Ask a medical or symptom question...")
    
    if user_input:
        # Append User Message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Process message
        with st.spinner("Processing medical query and screening for emergency triggers..."):
            result = orchestrator.process_user_message(
                user_message=user_input,
                chat_history=st.session_state.chat_messages,
                current_prediction=current_prediction,
                lang=lang
            )

        response_text = result["response"]

        # Append Assistant Response
        st.session_state.chat_messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            if result.get("is_emergency"):
                st.error(response_text)
            else:
                st.markdown(response_text)

            # Audio Playback option
            audio_bytes = SpeechService.text_to_speech(response_text, lang)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
