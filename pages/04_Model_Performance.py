import streamlit as st
from components.header import render_header
from components.language_controls import render_language_selector
from components.visualizations import plot_confusion_matrix, plot_metric_bar_chart
from training.evaluate_model import evaluate_specialist_performance
import json
import os

st.set_page_config(
    page_title="Model Performance — MediScope AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_header()
lang = render_language_selector()

st.markdown("""
<div style="margin-bottom: 20px;">
    <h2 style="margin: 0; color: #ffffff; font-weight: 800; letter-spacing: -0.02em;">📊 Neural Benchmark Validation & Evaluation Metrics</h2>
    <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
        Audited performance benchmarks, confusion matrices, latency metrics, and patient-level data partitions.
    </div>
</div>
""", unsafe_allow_html=True)

specialist = st.selectbox(
    "🎯 Select Specialist Model Architecture to Inspect:",
    options=["Chest Radiograph (DenseNet-121)", "Bone Fracture (YOLOv8 Detection)", "Ocular / Retinal (ResNet-50)", "Plant Disease (MobileNetV3)"]
)

if "Chest" in specialist:
    key = "chest"
    report = evaluate_specialist_performance("chest")
elif "Bone" in specialist:
    key = "fracture"
    report = evaluate_specialist_performance("fracture")
elif "Ocular" in specialist:
    key = "eye"
    report = evaluate_specialist_performance("eye")
else:
    key = "agriculture"
    report = evaluate_specialist_performance("agriculture")

# Row of KPI cards
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="metric-card-pro">
        <div class="kpi-label">Accuracy</div>
        <div class="kpi-val" style="color: #34d399 !important;">{report['accuracy']*100:.1f}%</div>
        <div class="kpi-sub">Test Split</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="metric-card-pro">
        <div class="kpi-label">Precision</div>
        <div class="kpi-val" style="color: #38bdf8 !important;">{report['precision']:.3f}</div>
        <div class="kpi-sub">Positive Predictive</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="metric-card-pro">
        <div class="kpi-label">Recall / Sens.</div>
        <div class="kpi-val" style="color: #818cf8 !important;">{report['recall']:.3f}</div>
        <div class="kpi-sub">True Positive Rate</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="metric-card-pro">
        <div class="kpi-label">F1-Score</div>
        <div class="kpi-val" style="color: #c084fc !important;">{report['f1_score']:.3f}</div>
        <div class="kpi-sub">Harmonic Mean</div>
    </div>
    """, unsafe_allow_html=True)
with k5:
    st.markdown(f"""
    <div class="metric-card-pro">
        <div class="kpi-label">Inference Latency</div>
        <div class="kpi-val" style="color: #f59e0b !important;">{report['avg_latency_ms']}ms</div>
        <div class="kpi-sub">{report['hardware']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""<div style="margin: 20px 0 16px 0;"></div>""", unsafe_allow_html=True)

col_m, col_chart = st.columns([1, 1])

with col_m:
    st.markdown(f"""
    <div class="glass-card" style="height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h4 style="margin: 0; color: #38bdf8;">📋 Detailed Telemetry Matrix</h4>
            <span class="pill-item pill-green">Verified</span>
        </div>
        <div style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.85;">
            <div>🧪 <strong>Validation Cohort:</strong> <code style="color: #38bdf8;">{report['test_samples']} clinical scans</code></div>
            <div>🛡️ <strong>Specificity (TNR):</strong> <code style="color: #34d399;">{report['specificity']:.3f}</code></div>
            <div>🔬 <strong>Sensitivity (TPR):</strong> <code style="color: #818cf8;">{report['sensitivity']:.3f}</code></div>
            {'<div>📍 <strong>mAP@0.5:</strong> <code>' + str(report.get("map_50", "")) + '</code> &nbsp;|&nbsp; <strong>mAP@0.5:0.95:</strong> <code>' + str(report.get("map_50_95", "")) + '</code></div>' if report.get("map_50") else ''}
            <div>💻 <strong>Hardware Target:</strong> <span style="color: #f8fafc;">{report['hardware']}</span></div>
            <div>⚡ <strong>Throughput:</strong> <span style="color: #34d399;">~{1000/max(1, report['avg_latency_ms']):.0f} frames/sec</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_chart:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    metrics_dict = {
        "Accuracy": report['accuracy'],
        "Precision": report['precision'],
        "Recall": report['recall'],
        "F1-Score": report['f1_score'],
        "Specificity": report['specificity']
    }
    fig = plot_metric_bar_chart(metrics_dict, f"{key.upper()} Specialist Performance")
    if fig is not None:
        st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""<div style="margin: 20px 0 16px 0; border-top: 1px solid rgba(255, 255, 255, 0.08);"></div>""", unsafe_allow_html=True)
st.markdown("### 🧩 Confusion Matrix & Validation Protocols")
cm = report["confusion_matrix"]
col_cm, col_protocol = st.columns([1, 1])

with col_cm:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    fig_cm = plot_confusion_matrix(cm["TP"], cm["FP"], cm["FN"], cm["TN"], f"{specialist} Matrix")
    if fig_cm is not None:
        st.pyplot(fig_cm)
    st.markdown('</div>', unsafe_allow_html=True)

with col_protocol:
    st.markdown("""
    <div class="glass-card" style="height: 100%; border-left: 4px solid #38bdf8;">
        <h4 style="color: #38bdf8; margin: 0 0 12px 0;">🛡️ Patient-Level Data Split Protocol</h4>
        <ul style="color: #cbd5e1; font-size: 0.88rem; padding-left: 18px; line-height: 1.8; margin-bottom: 0;">
            <li><strong>Zero Data Leakage:</strong> Dataset partitions are strictly isolated at the <strong>Patient ID level</strong>, ensuring no scan from the same patient spans training and testing splits.</li>
            <li><strong>Partition Ratios:</strong> 70% Training / 15% Cross-Validation / 15% Holdout Test.</li>
            <li><strong>Public Benchmark Provenance:</strong> NIH ChestX-ray14, Stanford MURA, APTOS 2019 Blindness, and PlantVillage datasets.</li>
            <li><strong>Bias Mitigation:</strong> Class imbalance compensated via focal loss weighting and balanced sampling.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
