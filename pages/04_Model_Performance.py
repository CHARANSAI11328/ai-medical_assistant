import streamlit as st
from components.header import render_header
from components.visualizations import plot_confusion_matrix, plot_metric_bar_chart
from training.evaluate_model import evaluate_specialist_performance
import json
import os

st.set_page_config(page_title="Model Performance — MediScope AI", page_icon="📊", layout="wide")

render_header()

st.title("📊 Model Performance & Evaluation Benchmarks")
st.markdown("Transparent performance metrics, confusion matrices, latency, and dataset provenance for all specialist models.")

specialist = st.selectbox(
    "Select Specialist Model to Inspect:",
    options=["Chest Radiograph (DenseNet-121)", "Bone Fracture (YOLOv8 Detection)", "Ocular / Retinal (ResNet-50)", "Plant Disease (MobileNetV3)"]
)

st.markdown("---")

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

col_m, col_chart = st.columns([1, 1])

with col_m:
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="color: #38bdf8; margin-top: 0;">📈 Performance Metrics ({specialist})</h3>
        <div style="font-size: 0.95rem; color: #cbd5e1; line-height: 1.8;">
            <div>🧪 <strong>Test Samples Evaluated:</strong> <code>{report['test_samples']}</code></div>
            <div>🎯 <strong>Accuracy:</strong> <span style="font-weight: 700; color: #34d399;">{report['accuracy']*100:.1f}%</span></div>
            <div>🎯 <strong>Precision:</strong> <code>{report['precision']:.3f}</code> &nbsp;|&nbsp; 🎯 <strong>Recall:</strong> <code>{report['recall']:.3f}</code></div>
            <div>📊 <strong>F1-Score:</strong> <code>{report['f1_score']:.3f}</code></div>
            <div>🔬 <strong>Sensitivity:</strong> <code>{report['sensitivity']:.3f}</code> &nbsp;|&nbsp; 🛡️ <strong>Specificity:</strong> <code>{report['specificity']:.3f}</code></div>
            {'<div>📍 <strong>mAP@0.5:</strong> <code>' + str(report.get("map_50", "")) + '</code> &nbsp;|&nbsp; <strong>mAP@0.5:0.95:</strong> <code>' + str(report.get("map_50_95", "")) + '</code></div>' if report.get("map_50") else ''}
            <div style="margin-top: 8px;">⚡ <strong>Average Inference Latency:</strong> <code style="color: #38bdf8;">{report['avg_latency_ms']} ms</code> per image</div>
            <div>💻 <strong>Hardware Benchmark:</strong> <code>{report['hardware']}</code></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_chart:
    metrics_dict = {
        "Accuracy": report['accuracy'],
        "Precision": report['precision'],
        "Recall": report['recall'],
        "F1-Score": report['f1_score'],
        "Specificity": report['specificity']
    }
    fig = plot_metric_bar_chart(metrics_dict, f"{key.upper()} Metric Distribution")
    if fig is not None:
        st.pyplot(fig)

st.markdown("---")
st.markdown("### 🧩 Confusion Matrix & Validation Protocol")
cm = report["confusion_matrix"]
col_cm, col_protocol = st.columns([1, 1])

with col_cm:
    fig_cm = plot_confusion_matrix(cm["TP"], cm["FP"], cm["FN"], cm["TN"], f"{specialist} Confusion Matrix")
    if fig_cm is not None:
        st.pyplot(fig_cm)

with col_protocol:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #38bdf8; margin-top: 0;">🛡️ Patient-Level Data Split Protocol</h4>
        <ul style="color: #cbd5e1; font-size: 0.9rem; padding-left: 18px; line-height: 1.7;">
            <li><strong>Data Leakage Prevention:</strong> Dataset splits are strictly partitioned at the <strong>Patient ID level</strong>, guaranteeing zero images from the same patient exist across training and evaluation splits.</li>
            <li><strong>Split Partition:</strong> 70% Training / 15% Validation / 15% Test.</li>
            <li><strong>Annotation Provenance:</strong> Validated against authorized public medical image repositories (NIH ChestX-ray14, MURA, APTOS 2019, PlantVillage).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
