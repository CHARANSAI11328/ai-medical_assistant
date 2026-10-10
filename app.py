import streamlit as st
from components.header import render_header
from components.language_controls import render_language_selector
from models.registry import ModelRegistry
from services.session_service import SessionService
import yaml
import os

st.set_page_config(
    page_title="MediScope AI — Multi-Specialist Diagnostic Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render Header
render_header()

# Sidebar Language Selection
lang = render_language_selector()

# Top KPI Metric Strip
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 16px;">
        <div style="color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Specialist Adapters</div>
        <div style="color: #38bdf8; font-size: 2.2rem; font-weight: 800; margin: 4px 0;">4 Vision Engines</div>
        <div style="color: #34d399; font-size: 0.8rem;">Eye · Chest · Bone · Crop</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 16px;">
        <div style="color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">LLM Intelligence</div>
        <div style="color: #818cf8; font-size: 2.2rem; font-weight: 800; margin: 4px 0;">Gemini 3.5</div>
        <div style="color: #c084fc; font-size: 0.8rem;">Structured Explanations</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 16px;">
        <div style="color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Visual Explainability</div>
        <div style="color: #f43f5e; font-size: 2.2rem; font-weight: 800; margin: 4px 0;">Grad-CAM & YOLO</div>
        <div style="color: #fb7185; font-size: 0.8rem;">Heatmaps & Bounding Boxes</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 16px;">
        <div style="color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Language Support</div>
        <div style="color: #34d399; font-size: 2.2rem; font-weight: 800; margin: 4px 0;">EN · HI · TE</div>
        <div style="color: #6ee7b7; font-size: 0.8rem;">Multilingual + Spoken Audio</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 🏥 Specialist Computer Vision Suite")

col1, col2 = st.columns([2, 1])

with col1:
    registry = ModelRegistry()
    specialists = registry.list_specialists()

    for spec in specialists:
        status_html = '<span class="pill-item pill-green">🟢 Active Neural Specialist</span>'
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 1.25rem; font-weight: 700; color: #f8fafc;">{spec['name']} <code style="font-size: 0.85rem; color: #38bdf8;">({spec['key'].upper()})</code></span>
                {status_html}
            </div>
            <div style="color: #94a3b8; font-size: 0.92rem; line-height: 1.6;">
                <div>📷 <strong>Modality:</strong> {spec['modality']}</div>
                <div>🎯 <strong>Task Architecture:</strong> <code>{spec['task_type']}</code> &nbsp;|&nbsp; 🎯 <strong>Confidence Threshold:</strong> <code>{spec['confidence_threshold']}</code></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #38bdf8; margin-top: 0;">⚡ Quick Walkthrough Guide</h4>
        <ol style="color: #cbd5e1; font-size: 0.9rem; padding-left: 20px; line-height: 1.7;">
            <li>Navigate to <strong>01 Medical Image Analysis</strong>.</li>
            <li>Click <strong>Analyze Sample 1</strong> (Eye), <strong>Sample 2</strong> (Chest), <strong>Sample 3</strong> (Fracture), or <strong>Sample 4</strong> (Crop Leaf).</li>
            <li>Inspect the <strong>Grad-CAM heatmap</strong> or <strong>YOLO bounding box</strong> visual.</li>
            <li>Review the structured Gemini plain-language medical breakdown.</li>
            <li>Listen to the <strong>spoken audio response</strong> & download your <strong>Markdown/JSON report</strong>.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #f43f5e;">
        <h4 style="color: #fb7185; margin-top: 0;">🛡️ Emergency Triage Layer</h4>
        <p style="color: #cbd5e1; font-size: 0.88rem; line-height: 1.5; margin-bottom: 0;">
            MediScope AI features automated safety screening. If red-flag emergency symptoms (acute chest pain, stroke signs, severe dyspnea) are detected, immediate priority guidance is triggered automatically.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("MediScope AI © 2026 — Research & Educational Platform. Not for independent medical diagnosis.")
