import streamlit as st
import os

def render_header():
    """
    Renders top header, app title, branding, and safety notice with 
    enterprise-grade cyber-clinical dark glassmorphism.
    Completely eliminates Streamlit default chrome and ensures crystal-clear contrast.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* 1. Complete Suppression of Streamlit Chrome & White Bar */
        header[data-testid="stHeader"],
        #MainMenu,
        footer,
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        .stDeployButton,
        div[data-testid="stSidebarCollapsedControl"],
        .viewerBadge_container__r5tak,
        [data-testid="manage-app-button"],
        .stAppDeployButton {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }

        /* 2. Global Canvas & Typography */
        :root {
            --bg-canvas: #070a12;
            --bg-card: rgba(15, 23, 42, 0.72);
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --border-glass: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(56, 189, 248, 0.35);
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --text-dim: #64748b;
            --accent-cyan: #38bdf8;
            --accent-indigo: #818cf8;
            --accent-emerald: #10b981;
            --accent-rose: #f43f5e;
            --accent-amber: #f59e0b;
        }

        html, body, [data-testid="stAppViewContainer"], .main, .block-container, section[data-testid="stMain"] {
            background-color: var(--bg-canvas) !important;
            color: var(--text-main) !important;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        .stApp {
            background: 
                radial-gradient(ellipse 90% 50% at 50% -12%, rgba(56, 189, 248, 0.12), transparent 70%),
                radial-gradient(ellipse 70% 45% at 90% 85%, rgba(99, 102, 241, 0.07), transparent 70%),
                radial-gradient(ellipse 60% 40% at 10% 70%, rgba(16, 185, 129, 0.05), transparent 70%),
                #070a12 !important;
            color: var(--text-main) !important;
        }

        .block-container {
            padding: 1.5rem 2.2rem 3rem !important;
            max-width: 1400px !important;
        }

        /* Enforce high contrast on all Markdown and Native text */
        p, span, label, li, td, th, h1, h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span {
            color: var(--text-main) !important;
            font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
        }

        h1, h2, h3 {
            font-weight: 700 !important;
            letter-spacing: -0.025em !important;
        }

        /* 3. Hero Header Section */
        .hero-container {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.75) 0%, rgba(30, 41, 59, 0.5) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-glass);
            border-radius: 18px;
            padding: 24px 28px;
            margin-bottom: 20px;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.12);
            position: relative;
            overflow: hidden;
        }

        .hero-container::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        }

        .main-title {
            background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 40%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.4rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .tagline {
            color: var(--text-sub) !important;
            font-size: 1.02rem;
            font-weight: 400;
            margin-bottom: 14px;
            line-height: 1.5;
        }

        /* Glowing Status Pills */
        .status-pill-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }

        .pill-item {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(56, 189, 248, 0.28);
            border-radius: 9999px;
            padding: 4px 13px;
            font-size: 0.8rem;
            font-weight: 600;
            color: #38bdf8 !important;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            letter-spacing: 0.01em;
            backdrop-filter: blur(8px);
            transition: all 0.25s ease;
        }

        .pill-item:hover {
            border-color: #38bdf8;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
            transform: translateY(-1px);
        }

        .pill-green {
            border-color: rgba(16, 185, 129, 0.35);
            color: #34d399 !important;
        }
        .pill-green:hover {
            border-color: #34d399;
            box-shadow: 0 0 12px rgba(52, 211, 153, 0.3);
        }

        .pill-purple {
            border-color: rgba(192, 132, 252, 0.35);
            color: #c084fc !important;
        }

        .pill-amber {
            border-color: rgba(245, 158, 11, 0.35);
            color: #fbbf24 !important;
        }

        /* Safety Notice Banner */
        .safety-banner {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(180, 83, 9, 0.08) 100%);
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-left: 4px solid #f59e0b;
            padding: 12px 18px;
            border-radius: 12px;
            font-size: 0.88rem;
            color: #fef3c7 !important;
            margin-bottom: 20px;
            line-height: 1.5;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 20px -6px rgba(0, 0, 0, 0.3);
        }
        .safety-banner strong {
            color: #fbbf24 !important;
        }

        /* 4. Glass Cards & Surfaces */
        .glass-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.72) 0%, rgba(20, 30, 52, 0.55) 100%);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.45);
        }

        .glass-card:hover {
            border-color: var(--border-glow);
            transform: translateY(-2px);
            box-shadow: 0 16px 36px -10px rgba(14, 165, 233, 0.25);
        }

        /* Metric Cards */
        .metric-card-pro {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(24, 34, 60, 0.6) 100%);
            border: 1px solid var(--border-glass);
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 10px 24px -5px rgba(0, 0, 0, 0.4);
            transition: all 0.25s ease;
            position: relative;
            overflow: hidden;
        }

        .metric-card-pro:hover {
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 14px 30px -8px rgba(56, 189, 248, 0.25);
        }

        .metric-card-pro .kpi-label {
            font-size: 0.78rem;
            color: var(--text-sub) !important;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 4px;
        }

        .metric-card-pro .kpi-val {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 1.85rem;
            font-weight: 800;
            color: #ffffff !important;
            letter-spacing: -0.02em;
            margin: 4px 0;
        }

        .metric-card-pro .kpi-sub {
            font-size: 0.78rem;
            color: var(--text-dim) !important;
            font-weight: 500;
        }

        /* 5. Streamlit Chat Overhaul (Ultra-High Contrast & Glassmorphism) */
        [data-testid="stChatMessage"] {
            border-radius: 14px !important;
            padding: 16px 20px !important;
            margin-bottom: 12px !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 0 8px 20px -5px rgba(0, 0, 0, 0.35) !important;
        }

        /* Assistant Bubble */
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]),
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatar"]:first-child) {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(23, 34, 58, 0.75) 100%) !important;
            border-left: 3px solid #38bdf8 !important;
        }

        /* User Bubble */
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(45, 59, 85, 0.75) 100%) !important;
            border-left: 3px solid #818cf8 !important;
        }

        /* Chat Message Text Content */
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] div {
            color: #f1f5f9 !important;
            font-size: 0.96rem !important;
            line-height: 1.65 !important;
        }

        /* Chat Input Box */
        [data-testid="stChatInput"] {
            background: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid rgba(56, 189, 248, 0.35) !important;
            border-radius: 14px !important;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.6) !important;
            transition: all 0.25s ease !important;
        }

        [data-testid="stChatInput"]:focus-within {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.3) !important;
        }

        [data-testid="stChatInput"] textarea {
            color: #f8fafc !important;
            font-size: 0.95rem !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #64748b !important;
        }

        [data-testid="stChatInput"] button {
            color: #38bdf8 !important;
        }

        /* 6. Sidebar Overhaul */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b0f19 0%, #070a12 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 10px 0 30px rgba(0, 0, 0, 0.4) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
        section[data-testid="stSidebar"] label {
            color: #cbd5e1 !important;
        }

        /* Sidebar Navigation Links */
        [data-testid="stSidebarNav"] {
            padding-top: 10px !important;
        }

        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNavLink"] {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            margin-bottom: 6px !important;
            padding: 8px 14px !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stSidebarNavLink"] span {
            color: #e2e8f0 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }

        [data-testid="stSidebarNavLink"]:hover {
            background: rgba(56, 189, 248, 0.12) !important;
            border-color: rgba(56, 189, 248, 0.35) !important;
            transform: translateX(4px) !important;
        }

        [data-testid="stSidebarNavLink"]:hover span {
            color: #38bdf8 !important;
        }

        [data-testid="stSidebarNavLink"][aria-current="page"] {
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.22) 0%, rgba(99, 102, 241, 0.18) 100%) !important;
            border: 1px solid rgba(56, 189, 248, 0.55) !important;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.2) !important;
        }

        [data-testid="stSidebarNavLink"][aria-current="page"] span {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        /* 7. Buttons Overhaul */
        .stButton > button {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
            border-radius: 10px !important;
            padding: 8px 18px !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
        }

        .stButton > button:hover {
            border-color: #38bdf8 !important;
            color: #38bdf8 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px -4px rgba(56, 189, 248, 0.4) !important;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 6px 20px -4px rgba(79, 70, 229, 0.5) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #0369a1 0%, #4338ca 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 25px -4px rgba(79, 70, 229, 0.7) !important;
        }

        /* 8. Inputs, Selectboxes, and File Dropzone */
        div[data-baseweb="select"] > div {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: #f8fafc !important;
        }

        div[data-baseweb="input"] > div {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: #f8fafc !important;
        }

        [data-testid="stFileUploader"] {
            background: rgba(15, 23, 42, 0.5) !important;
            border: 2px dashed rgba(56, 189, 248, 0.3) !important;
            border-radius: 14px !important;
            padding: 16px !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #38bdf8 !important;
            background: rgba(15, 23, 42, 0.75) !important;
        }

        /* Progress Bar Fills */
        [data-testid="stProgress"] > div > div {
            background: linear-gradient(90deg, #38bdf8 0%, #34d399 100%) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.5) !important;
        }

        /* Expanders */
        [data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
        }

        /* Suggestion Chips */
        .chip-btn {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 0.82rem;
            color: #cbd5e1;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
        }
        .chip-btn:hover {
            border-color: #38bdf8;
            color: #38bdf8;
            background: rgba(56, 189, 248, 0.1);
        }

        /* Audio Player Styling */
        audio {
            width: 100%;
            margin-top: 8px;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-container">
            <div class="main-title">🏥 MediScope AI</div>
            <div class="tagline">Next-Generation Multi-Specialist AI Medical Diagnostic & Educational Platform</div>
            <div class="status-pill-group">
                <span class="pill-item pill-green">🟢 Gemini 3.5 Active Engine</span>
                <span class="pill-item">🔬 Grad-CAM & YOLOv8 Vision</span>
                <span class="pill-item pill-purple">🌐 Multilingual (EN · HI · TE)</span>
                <span class="pill-item pill-amber">🛡️ Safety Triage Screener</span>
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
