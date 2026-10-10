import streamlit as st
import yaml
import os

def render_header():
    """Renders top header, app title, branding, and safety notice with world-class glassmorphic styling."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

        /* Global Canvas Background */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 50%, #090d16 100%);
            color: #f8fafc;
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
        }

        /* Animated Hero Header */
        .hero-container {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 24px 30px;
            margin-bottom: 24px;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }

        .main-title {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.6rem;
            font-weight: 800;
            letter-spacing: -0.8px;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .tagline {
            color: #94a3b8;
            font-size: 1.1rem;
            font-weight: 400;
            margin-bottom: 16px;
        }

        /* Pill Badge Indicators */
        .status-pill-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 12px;
        }
        .pill-item {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 20px;
            padding: 5px 14px;
            font-size: 0.82rem;
            font-weight: 600;
            color: #38bdf8;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .pill-green {
            border-color: rgba(52, 211, 153, 0.3);
            color: #34d399;
        }
        .pill-purple {
            border-color: rgba(192, 132, 252, 0.3);
            color: #c084fc;
        }

        /* Glassmorphic Cards */
        .glass-card {
            background: rgba(30, 41, 59, 0.55);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 18px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        .glass-card:hover {
            border-color: rgba(56, 189, 248, 0.35);
            transform: translateY(-3px);
            box-shadow: 0 15px 35px -10px rgba(14, 165, 233, 0.25);
        }

        /* Safety Banner */
        .safety-banner {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.08) 100%);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-left: 5px solid #f59e0b;
            padding: 14px 20px;
            border-radius: 12px;
            font-size: 0.92rem;
            color: #fef3c7;
            margin-bottom: 22px;
            line-height: 1.55;
            backdrop-filter: blur(10px);
        }

        /* Streamlit Button Overhaul */
        .stButton > button {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #f8fafc;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 8px 18px;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.25s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        .stButton > button:hover {
            border-color: #38bdf8;
            color: #38bdf8;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px -4px rgba(56, 189, 248, 0.4);
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%);
            color: #ffffff;
            border: none;
            box-shadow: 0 6px 20px -4px rgba(79, 70, 229, 0.5);
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #0369a1 0%, #4338ca 100%);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -4px rgba(79, 70, 229, 0.7);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        /* File Uploader Dropzone */
        [data-testid="stFileUploader"] {
            background: rgba(30, 41, 59, 0.4);
            border: 2px dashed rgba(56, 189, 248, 0.3);
            border-radius: 14px;
            padding: 16px;
            transition: all 0.3s ease;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #38bdf8;
            background: rgba(30, 41, 59, 0.7);
        }

        /* Progress Bar Fills */
        [data-testid="stProgress"] > div > div {
            background: linear-gradient(90deg, #38bdf8 0%, #34d399 100%) !important;
            border-radius: 10px;
        }

        /* Expander Containers */
        [data-testid="stExpander"] {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-container">
            <div class="main-title">🏥 MediScope AI</div>
            <div class="tagline">Next-Generation Multi-Specialist AI Medical Diagnostic & Educational Platform</div>
            <div class="status-pill-group">
                <span class="pill-item pill-green">🟢 Gemini 3.5 Live Engine</span>
                <span class="pill-item">🔬 Grad-CAM & YOLOv8 Vision</span>
                <span class="pill-item pill-purple">🌐 Multilingual (EN/HI/TE)</span>
                <span class="pill-item">🛡️ Emergency Triage Active</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="safety-banner">
        <strong>⚠️ Clinical Research Notice:</strong> MediScope AI is an advanced AI research & educational prototype, 
        <strong>NOT a certified medical diagnostic device</strong>. Model predictions require expert medical verification. 
        Always seek immediate professional medical attention for any health emergency.
    </div>
    """, unsafe_allow_html=True)
