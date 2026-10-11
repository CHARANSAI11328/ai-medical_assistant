import streamlit as st
from PIL import Image, ImageDraw

def generate_sample_demo_images() -> dict:
    """Generates synthetic authorized clinical sample images for walkthroughs."""
    sample_images = {}

    # 1. Sample Retinal Fundus (Red circular gradient with optic disc)
    img_eye = Image.new("RGB", (300, 300), color=(25, 6, 6))
    draw = ImageDraw.Draw(img_eye)
    draw.ellipse([30, 30, 270, 270], fill=(185, 40, 18), outline=(245, 195, 75), width=4)
    draw.ellipse([180, 120, 230, 170], fill=(255, 235, 170))  # Optic disc
    draw.line([190, 140, 120, 100], fill=(130, 20, 10), width=2)
    draw.line([190, 150, 100, 180], fill=(130, 20, 10), width=2)
    sample_images["Ocular Retinal Scan"] = {
        "img": img_eye,
        "modality": "Retinal Fundus",
        "spec": "Eye Specialist"
    }

    # 2. Sample Chest X-Ray (Bilateral pulmonary field grayscale)
    img_chest = Image.new("RGB", (300, 300), color=(35, 38, 45))
    draw = ImageDraw.Draw(img_chest)
    draw.ellipse([40, 50, 130, 240], fill=(155, 158, 168))
    draw.ellipse([170, 50, 260, 240], fill=(145, 148, 158))
    draw.rectangle([130, 100, 170, 210], fill=(85, 88, 98))  # Cardiac silhouette
    sample_images["Chest Radiograph"] = {
        "img": img_chest,
        "modality": "Pulmonary X-Ray",
        "spec": "Chest Specialist"
    }

    # 3. Sample Bone Fracture Radiograph
    img_bone = Image.new("RGB", (250, 350), color=(25, 27, 34))
    draw = ImageDraw.Draw(img_bone)
    draw.rectangle([100, 30, 150, 320], fill=(205, 208, 220))  # Bone shaft
    draw.line([100, 160, 150, 175], fill=(18, 18, 22), width=5)  # Fracture line
    sample_images["Bone Radiograph"] = {
        "img": img_bone,
        "modality": "Skeletal X-Ray",
        "spec": "Fracture Specialist"
    }

    # 4. Sample Agriculture Crop Leaf
    img_leaf = Image.new("RGB", (300, 300), color=(230, 235, 240))
    draw = ImageDraw.Draw(img_leaf)
    draw.ellipse([60, 40, 240, 260], fill=(38, 155, 50), outline=(18, 85, 28), width=3)
    draw.ellipse([100, 100, 150, 150], fill=(155, 85, 25))  # Rust lesion spot
    sample_images["Crop Leaf Pathology"] = {
        "img": img_leaf,
        "modality": "Foliar Photo",
        "spec": "Plant Specialist"
    }

    return sample_images

def render_image_uploader():
    """Renders clinical PACS-style scan selector, modality chooser, and file uploader."""
    st.markdown("""
    <div style="margin-bottom: 14px;">
        <h3 style="margin: 0; color: #ffffff; font-weight: 700;">📤 Clinical Scan Ingestion & Modality Routing</h3>
        <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 2px;">
            Select an authorized clinical sample for instant validation, or upload a medical imaging file.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_modality, col_upload = st.columns([1, 2])

    with col_modality:
        modality_options = {
            "Auto-Detect Modality": "auto",
            "Retinal / Eye Photograph": "eye",
            "Chest X-Ray": "chest",
            "Bone Radiograph (X-Ray)": "fracture",
            "Plant / Crop Leaf": "agriculture"
        }
        selected_label = st.selectbox(
            "🎯 Specialist Router Target:",
            options=list(modality_options.keys()),
            index=0
        )
        modality_key = modality_options[selected_label]

    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload Clinical Scan (JPG, PNG)",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear medical radiograph, fundus photo, or crop leaf image."
        )

    st.markdown("""
    <div style="color: #cbd5e1; font-weight: 600; font-size: 0.88rem; margin: 16px 0 10px 0; display: flex; align-items: center; gap: 6px;">
        <span>⚡</span> Instant Clinical Benchmark Samples (One-Click Ingestion):
    </div>
    """, unsafe_allow_html=True)

    sample_dict = generate_sample_demo_images()
    demo_cols = st.columns(len(sample_dict))

    for idx, (name, data) in enumerate(sample_dict.items()):
        img = data["img"]
        modality_tag = data["modality"]
        spec_label = data["spec"]

        with demo_cols[idx]:
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); 
                        border-radius: 12px; padding: 10px; text-align: center; margin-bottom: 6px;">
                <div style="font-weight: 700; color: #f8fafc; font-size: 0.82rem; margin-bottom: 2px;">{name}</div>
                <div style="color: #38bdf8; font-size: 0.72rem; font-weight: 600;">{modality_tag}</div>
            </div>
            """, unsafe_allow_html=True)
            st.image(img, use_container_width=True)
            if st.button(f"Analyze Sample {idx+1}", key=f"demo_btn_{idx}", use_container_width=True):
                st.session_state.active_image = img
                st.session_state.active_image_name = name
                # Clear old predictions when new sample is selected
                st.session_state.pop("active_prediction", None)
                st.session_state.pop("active_explanation", None)
                st.rerun()

    if uploaded_file is not None:
        try:
            st.session_state.active_image = Image.open(uploaded_file)
            st.session_state.active_image_name = uploaded_file.name
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")

    final_img = st.session_state.get("active_image", None)
    img_name = st.session_state.get("active_image_name", "Uploaded Scan")

    return final_img, img_name, modality_key
