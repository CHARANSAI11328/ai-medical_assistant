import streamlit as st
from services.medical_assistant import MedicalAssistantOrchestrator
from services.speech_service import SpeechService
from services.gemini_service import GeminiMedicalService

def render_chatbot(current_prediction=None, lang: str = "en"):
    """
    Renders enterprise-grade interactive medical conversational assistant chat UI
    with active clinical scan context, quick question chips, high-contrast messages,
    and voice synthesis.
    """
    # 1. Top Control Bar
    c_title, c_status, c_reset = st.columns([3, 2, 1])
    
    with c_title:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px;">
            <h3 style="margin: 0; color: #f8fafc; font-weight: 700;">💬 Clinical Conversation & Triage</h3>
        </div>
        """, unsafe_allow_html=True)

    with c_status:
        gemini_svc = GeminiMedicalService()
        if gemini_svc.is_available and gemini_svc.api_key:
            st.markdown("""
            <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.15); 
                        border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 9999px; padding: 4px 12px; font-size: 0.78rem; font-weight: 600; color: #34d399;">
                <span style="height: 7px; width: 7px; background-color: #34d399; border-radius: 50%; display: inline-block;"></span>
                <span>Gemini 3.5 Live & Connected</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(56, 189, 248, 0.12); 
                        border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 9999px; padding: 4px 12px; font-size: 0.78rem; font-weight: 600; color: #38bdf8;">
                <span style="height: 7px; width: 7px; background-color: #38bdf8; border-radius: 50%; display: inline-block;"></span>
                <span>Offline Reasoning Engine</span>
            </div>
            """, unsafe_allow_html=True)

    with c_reset:
        if st.button("🔄 Clear Chat", key="clear_chat_btn", use_container_width=True):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Hello! I am your MediScope AI Medical Information Assistant. How can I help you with medical concepts, symptoms, or scan results today?"}
            ]
            st.rerun()

    # 2. Attached Active Scan Context Banner (if user ran a scan)
    if current_prediction:
        spec_name = current_prediction.get("specialist_name", "Specialist Model")
        pred_label = current_prediction.get("predicted_label", "Unknown")
        conf_val = current_prediction.get("confidence", 0.0) * 100
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(99, 102, 241, 0.1) 100%); 
                    border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 12px 18px; margin: 12px 0 16px 0;
                    display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.2rem;">📎</span>
                <div>
                    <div style="font-size: 0.76rem; color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Active Scan Context Attached</div>
                    <div style="color: #f8fafc; font-weight: 600; font-size: 0.92rem;">{spec_name}: <code style="color: #38bdf8; background: rgba(56, 189, 248, 0.15); padding: 1px 6px; border-radius: 4px;">{pred_label}</code> ({conf_val:.1f}% confidence)</div>
                </div>
            </div>
            <span class="pill-item pill-green">Context Sync ON</span>
        </div>
        """, unsafe_allow_html=True)

    # 3. Interactive Quick Questions / Starter Chips
    st.markdown("""
    <div style="color: #94a3b8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin: 10px 0 8px 0;">
        💡 Suggested Clinical Queries:
    </div>
    """, unsafe_allow_html=True)

    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    quick_query = None

    with q_col1:
        if st.button("🩺 Explain Attached Scan", key="quick_q1", use_container_width=True):
            quick_query = "Please explain the clinical meaning of the attached medical scan finding in simple terms."
    with q_col2:
        if st.button("👁️ Retinal & Eye Health", key="quick_q2", use_container_width=True):
            quick_query = "What are the early warning signs of diabetic retinopathy or glaucoma?"
    with q_col3:
        if st.button("🫁 Chest X-Ray Findings", key="quick_q3", use_container_width=True):
            quick_query = "What does pulmonary consolidation or opacity usually indicate on a chest radiograph?"
    with q_col4:
        if st.button("🚨 Emergency Chest Pain", key="quick_q4", use_container_width=True):
            quick_query = "I am having sudden crushing chest pain radiating to my left arm. What should I do?"

    # Initialize messages
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! I am your MediScope AI Medical Information Assistant. How can I help you with medical concepts, symptoms, or scan results today?"}
        ]

    # Render previous messages
    st.markdown("""<div style="margin: 16px 0;"></div>""", unsafe_allow_html=True)
    
    for msg in st.session_state.chat_messages:
        role = msg["role"]
        avatar = "🏥" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask a medical or symptom question...")
    
    # Process if quick query clicked or user entered text
    message_to_send = user_input or quick_query

    if message_to_send:
        # Append User Message
        st.session_state.chat_messages.append({"role": "user", "content": message_to_send})
        with st.chat_message("user", avatar="👤"):
            st.markdown(message_to_send)

        # Process message with spinner
        orchestrator = MedicalAssistantOrchestrator()
        with st.spinner("Analyzing medical query & screening for critical emergency triggers..."):
            result = orchestrator.process_user_message(
                user_message=message_to_send,
                chat_history=st.session_state.chat_messages,
                current_prediction=current_prediction,
                lang=lang
            )

        response_text = result["response"]
        is_emergency = result.get("is_emergency", False)

        # Append Assistant Response
        st.session_state.chat_messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant", avatar="🏥"):
            if is_emergency:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(185, 28, 28, 0.15) 100%);
                            border: 1px solid rgba(239, 68, 68, 0.5); border-left: 5px solid #ef4444; border-radius: 12px;
                            padding: 16px 20px; margin-bottom: 12px; box-shadow: 0 0 25px rgba(239, 68, 68, 0.3);">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <span style="font-size: 1.3rem;">🚨</span>
                        <strong style="color: #fca5a5; font-size: 1.05rem;">URGENT CLINICAL TRIAGE ALERT</strong>
                    </div>
                    <div style="color: #fef2f2; line-height: 1.6; font-size: 0.95rem;">{response_text}</div>
                    <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(239, 68, 68, 0.3);
                                display: flex; gap: 12px; font-weight: 700; font-size: 0.88rem; color: #fecaca;">
                        <span>📞 Emergency US: 911</span>
                        <span>·</span>
                        <span>📞 Emergency EU: 112</span>
                        <span>·</span>
                        <span>📞 Emergency India: 108 / 102</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(response_text)

            # Audio Playback
            audio_bytes = SpeechService.text_to_speech(response_text, lang)
            if audio_bytes:
                st.markdown("""
                <div style="margin-top: 10px; color: #94a3b8; font-size: 0.78rem; font-weight: 600;">
                    🔊 Spoken Audio Explanation:
                </div>
                """, unsafe_allow_html=True)
                st.audio(audio_bytes, format="audio/mp3")

        st.rerun()
