import streamlit as st
from components.header import render_header
from services.session_service import SessionService

st.set_page_config(page_title="About, Privacy & Safety — MediScope AI", page_icon="🛡️", layout="wide")

render_header()

st.title("🛡️ About, Privacy, Safety & Disclaimers")

st.markdown("""
### 🏥 Purpose & Scope of MediScope AI
**MediScope AI** is an AI-assisted medical information and computer vision research prototype built to demonstrate multi-specialist image routing, Grad-CAM attribution, YOLO object localization, and conversational medical assistance.

---

### ⚠️ Critical Medical & Safety Disclaimers
1. **Not a Licensed Medical Device:** MediScope AI is **NOT** a certified medical diagnostic device and cannot provide a binding clinical diagnosis or treatment recommendation.
2. **False Positives & False Negatives:** Model predictions may be inaccurate. A negative result or low confidence score does **NOT** rule out a medical condition.
3. **Emergency Care Directive:** In the event of acute, severe, or life-threatening symptoms (such as chest pain, severe shortness of breath, stroke symptoms, sudden vision loss, or uncontrolled bleeding), **immediately contact local emergency services (911 / 112 / 108)** or visit the nearest emergency department.

---

### 🔒 Privacy & Data Handling Policy
- **Zero Retained Patient Metadata:** Uploaded images have all EXIF headers and metadata automatically stripped before processing.
- **Transient Memory Storage:** Uploaded image files are processed in memory and are **NOT** stored permanently on disk or logged to external databases.
- **Session Privacy Purge:** Users can purge all active conversation state and session history at any time using the control below.
""")

st.markdown("---")
st.markdown("### 🧹 Session Data Purge (Privacy Control)")
if st.button("🗑️ Reset All Session History & Clear Active Scans", type="primary"):
    session_svc = SessionService()
    session_svc.clear_session_data()
    st.session_state.clear()
    st.success("✅ All session history, cached predictions, and chat context have been completely purged from memory.")
