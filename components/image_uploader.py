import streamlit as st
from PIL import Image, ImageDraw

def generate_sample_demo_images() -> dict:
    """Generates synthetic authorized clinical sample images for walkthroughs."""
    sample_images = {}

    # 1. Sample Retinal Fundus (Red circular gradient)
    img_eye = Image.new("RGB", (300, 300), color=(30, 5, 5))
    draw = ImageDraw.Draw(img_eye)
    draw.ellipse([30, 30, 270, 270], fill=(190, 45, 20), outline=(240, 200, 80), width=4)
    draw.ellipse([180, 120, 230, 170], fill=(255, 240, 180))  # Optic disc
    sample_images["Ocular Retinal Scan"] = img_eye

    # 2. Sample Chest X-Ray (Bilateral pulmonary field grayscale)
    img_chest = Image.new("RGB", (300, 300), color=(40, 40, 45))
    draw = ImageDraw.Draw(img_chest)
    draw.ellipse([40, 50, 130, 240], fill=(160, 160, 170))
    draw.ellipse([170, 50, 260, 240], fill=(150, 150, 160))
    draw.rectangle([130, 100, 170, 210], fill=(90, 90, 100))  # Cardiac silhouette
    sample_images["Chest Radiograph"] = img_chest

    # 3. Sample Bone Fracture Radiograph
    img_bone = Image.new("RGB", (250, 350), color=(30, 30, 35))
    draw = ImageDraw.Draw(img_bone)
    draw.rectangle([100, 30, 150, 320], fill=(210, 210, 220))  # Bone shaft
    draw.line([100, 160, 150, 175], fill=(20, 20, 25), width=4)  # Fracture line
    sample_images["Bone Radiograph"] = img_bone

    # 4. Sample Agriculture Crop Leaf
    img_leaf = Image.new("RGB", (300, 300), color=(240, 240, 240))
    draw = ImageDraw.Draw(img_leaf)
    draw.ellipse([60, 40, 240, 260], fill=(40, 160, 50), outline=(20, 90, 30), width=3)
    draw.ellipse([100, 100, 150, 150], fill=(160, 90, 30))  # Rust lesion spot
    sample_images["Crop Leaf Pathology"] = img_leaf

    return sample_images

def render_image_uploader():
    """Renders image uploader, modality dropdown, and sample image picker."""
    st.markdown("### 📤 Step 1: Upload Scan or Select Sample Image")
    
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
            "🎯 Select Modality Specialist:",
            options=list(modality_options.keys()),
            index=0
        )
        modality_key = modality_options[selected_label]

    sample_images = generate_sample_demo_images()

    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload image (JPG, PNG)",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear medical scan or plant leaf photo."
        )

    st.markdown("**or Select Sample Scan for Instant Analysis:**")
    demo_cols = st.columns(len(sample_images))

    for idx, (name, img) in enumerate(sample_images.items()):
        with demo_cols[idx]:
            st.image(img, use_container_width=True, caption=name)
            if st.button(f"Analyze Sample {idx+1}", key=f"demo_btn_{idx}"):
                st.session_state.active_image = img
                st.session_state.active_image_name = name
                # Clear old predictions when new sample is clicked
                st.session_state.pop("active_prediction", None)
                st.session_state.pop("active_explanation", None)

    if uploaded_file is not None:
        try:
            st.session_state.active_image = Image.open(uploaded_file)
            st.session_state.active_image_name = uploaded_file.name
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")

    final_img = st.session_state.get("active_image", None)
    img_name = st.session_state.get("active_image_name", "Uploaded Scan")

    return final_img, img_name, modality_key
