import streamlit as st
from components.header import render_header
from components.language_controls import render_language_selector
from models.registry import ModelRegistry
from services.session_service import SessionService
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

# Top KPI Metric Strip (Enterprise SaaS Metric Cards)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown("""
    <div class="metric-card-pro">
        <div class="kpi-label">Specialist Adapters</div>
        <div class="kpi-val" style="color: #38bdf8 !important;">4 Engines</div>
        <div class="kpi-sub" style="color: #34d399 !important;">● Eye · Chest · Bone · Crop</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card-pro">
        <div class="kpi-label">Reasoning Engine</div>
        <div class="kpi-val" style="color: #818cf8 !important;">Gemini 3.5</div>
        <div class="kpi-sub" style="color: #c084fc !important;">● Structured Clinical Guidance</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card-pro">
        <div class="kpi-label">Explainability</div>
        <div class="kpi-val" style="color: #f43f5e !important;">Grad-CAM</div>
        <div class="kpi-sub" style="color: #fb7185 !important;">● YOLOv8 Bounding Boxes</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-card-pro">
        <div class="kpi-label">Language Support</div>
        <div class="kpi-val" style="color: #34d399 !important;">EN · HI · TE</div>
        <div class="kpi-sub" style="color: #6ee7b7 !important;">● Voice Playback Accessible</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""<div style="margin: 20px 0 10px 0;"></div>""", unsafe_allow_html=True)

# Specialist Computer Vision Suite
col1, col2 = st.columns([13, 8])

with col1:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
        <h3 style="margin: 0; color: #ffffff; font-weight: 700;">🔬 Active Neural Specialist Suite</h3>
        <span class="pill-item pill-green">All Models Operational</span>
    </div>
    """, unsafe_allow_html=True)

    registry = ModelRegistry()
    specialists = registry.list_specialists()

    icons = {
        "eye": "👁️",
        "chest": "🫁",
        "fracture": "🦴",
        "agriculture": "🌿"
    }

    modality_tags = {
        "eye": "#38bdf8",
        "chest": "#818cf8",
        "fracture": "#fb7185",
        "agriculture": "#34d399"
    }

    for spec in specialists:
        s_key = spec['key']
        icon = icons.get(s_key, "🔬")
        tag_color = modality_tags.get(s_key, "#38bdf8")

        st.markdown(f"""
        <div class="glass-card" style="padding: 18px 22px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                <div>
                    <span style="font-size: 1.15rem; font-weight: 700; color: #ffffff;">{icon} {spec['name']}</span>
                    <span style="background: rgba(255,255,255,0.06); color: {tag_color}; font-size: 0.76rem; font-weight: 700; 
                                 padding: 2px 8px; border-radius: 6px; margin-left: 8px; border: 1px solid rgba(255,255,255,0.1);">
                        {spec['key'].upper()}
                    </span>
                </div>
                <span class="pill-item pill-green">Ready</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.88rem; color: #94a3b8;">
                <div>📷 <strong>Modality:</strong> <span style="color: #e2e8f0;">{spec['modality']}</span></div>
                <div>🎯 <strong>Architecture:</strong> <code style="color: {tag_color};">{spec['task_type']}</code></div>
                <div>⚡ <strong>Threshold:</strong> <span style="color: #e2e8f0;">{spec['confidence_threshold']}</span></div>
                <div>🔍 <strong>Explainability:</strong> <span style="color: #e2e8f0;">Grad-CAM / BBoxes</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card" style="border-top: 3px solid #38bdf8;">
        <h4 style="color: #38bdf8; margin: 0 0 12px 0; font-size: 1.05rem; display: flex; align-items: center; gap: 6px;">
            <span>⚡</span> Quick Diagnostic Walkthrough
        </h4>
        <ol style="color: #cbd5e1; font-size: 0.88rem; padding-left: 20px; line-height: 1.8; margin-bottom: 0;">
            <li>Switch to <strong>01 Medical Image Analysis</strong> from the left sidebar.</li>
            <li>Click any instant clinical sample (Retinal, Chest, Bone, Foliar Leaf) or upload a custom DICOM/PNG/JPG scan.</li>
            <li>Inspect the automated <strong>Grad-CAM attention heatmap</strong> or <strong>YOLO localization bbox</strong>.</li>
            <li>Review the structured <strong>plain-language medical breakdown</strong> generated by Gemini 3.5.</li>
            <li>Listen to accessible <strong>spoken audio</strong> & export your <strong>clinical summary report</strong>.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #ef4444; border-top: 1px solid rgba(239, 68, 68, 0.3);">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span style="font-size: 1.15rem;">🛡️</span>
            <strong style="color: #fca5a5; font-size: 0.95rem;">Automated Emergency Triage Shield</strong>
        </div>
        <p style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.6; margin-bottom: 0;">
            MediScope AI features continuous safety screening. If red-flag emergency symptoms (acute chest pain, dyspnea, neurological signs) are detected, immediate priority guidance is triggered with emergency dispatch hotlines.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""<div style="margin: 20px 0; border-top: 1px solid rgba(255, 255, 255, 0.08);"></div>""", unsafe_allow_html=True)
st.caption("MediScope AI © 2026 — Research & Educational Platform. Not for independent medical diagnosis.")
