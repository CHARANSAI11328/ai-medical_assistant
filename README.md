# 🏥 MediScope AI — AI-Powered Multi-Specialist Medical Diagnostic Assistant

**MediScope AI** is a multi-specialist computer vision and conversational AI research prototype built to assist users with medical image analysis, plain-language educational guidance, and multilingual symptom support.

---

## 🚀 Key Features

- **🔬 Multi-Specialist Computer Vision Architecture:**
  - **Ocular & Retinal Specialist:** Analyzes fundus photos for Diabetic Retinopathy, Glaucoma, Cataracts, and AMD using ResNet-50.
  - **Chest X-Ray Specialist:** Evaluates chest radiographs for Pneumonia, Tuberculosis, Effusion, and Cardiomegaly using DenseNet-121.
  - **Bone Fracture Specialist:** Detects and localizes fractures and dislocations with YOLOv8 bounding boxes.
  - **Agricultural Crop Specialist:** Identifies foliar blights, rusts, and leaf spots on crop plants using MobileNetV3.
- **🔥 Visual Explainability:** Genuine Grad-CAM heatmaps for classification attention and YOLO bounding boxes for object localization.
- **💬 Gemini 3.5 Educational Assistant:** Generates structured plain-language medical breakdowns and answers questions in **English, Hindi, and Telugu**.
- **🚨 Safety Triage Layer:** Automated symptom screening to flag emergency symptoms (chest pain, stroke signs) and prioritize immediate medical care.
- **🔊 Spoken Voice Responses:** Multilingual text-to-speech audio synthesis.
- **📈 Transparent Evaluation & Training Pipeline:** Reproducible training scripts for custom YOLO models and full evaluation benchmark suites.
- **📄 Session Report Export:** Downloadable Markdown and raw JSON reports.

---

## 🛠️ Project Architecture

```
ai_medical_assistant/
├── app.py                      # Main Streamlit Dashboard & Landing Page
├── pages/
│   ├── 01_Medical_Image_Analysis.py
│   ├── 02_AI_Medical_Assistant.py
│   ├── 03_Agriculture_AI.py
│   ├── 04_Model_Performance.py
│   └── 05_About_and_Safety.py
├── components/                 # Reusable Streamlit UI Widgets
├── models/                     # Specialist Model Adapters, Registry & Router
├── services/                   # Gemini LLM, Triage, Preprocessing, Speech, Reports
├── training/                   # YOLO & PyTorch Classifier Training & Evaluation Scripts
├── datasets/                   # Dataset Configuration & Sample Data
├── evaluation/                 # Benchmark Reports & Test Cases
├── tests/                      # Pytest Automated Test Suite
├── configs/                    # YAML Configurations
└── BUG_AUDIT.md                # Comprehensive Bug Audit & Repair Log
```

---

## ⚙️ Installation & Local Setup

### 1. Prerequisites
- Python 3.10+ installed
- Git

### 2. Virtual Environment Setup
```bash
# Navigate to project directory
cd d:\ml-workshop\ai_medical_assistant

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
py -3 -m pip install -r requirements.txt
```

### 4. Configure Environment Variables
In `.env`:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GOOGLE_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
```

---

## 🖥️ Launching the Application

Run the Streamlit application with:
```bash
py -3 -m streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 🏋️ Training & Evaluation Commands

### 1. Dataset Preparation & Split Generation
```bash
py -3 -m training.prepare_dataset --output-dir datasets/sample_data
```

### 2. Custom YOLO Fracture Model Training
```bash
py -3 -m training.train_yolo --config training/dataset_config/fracture_yolo.yaml --epochs 10 --model-size yolov8n.pt
```

### 3. Model Evaluation & Benchmark Report Generation
```bash
py -3 -m training.evaluate_model --specialist chest --output evaluation/reports/chest_eval.json
```

---

## 🧪 Running Automated Tests

Run all unit test suites using Python:
```bash
py -3 tests/test_triage.py
py -3 tests/test_preprocessing.py
py -3 tests/test_routing.py
py -3 tests/test_models.py
```

---

## 🎯 Judge Demonstration Walkthrough Guide

1. Launch `py -3 -m streamlit run app.py`.
2. Navigate to **01 Medical Image Analysis**.
3. Under **Select Judge Walkthrough Demo Image**, click any sample:
   - **Demo 1 (Eye):** Runs Retinal Specialist -> Displays Grad-CAM heatmap -> Gemini explanation -> Audio player.
   - **Demo 2 (Chest):** Runs Chest X-Ray Specialist -> Displays pulmonary Grad-CAM heatmap.
   - **Demo 3 (Bone Fracture):** Runs YOLO Fracture Specialist -> Displays red YOLO bounding box localization.
   - **Demo 4 (Crop Leaf):** Runs Agriculture Specialist -> Displays leaf lesion heatmap.
4. Navigate to **02 AI Medical Assistant** and type `"I have severe chest pain"` to test the **Emergency Safety Triage Alert**.
5. Navigate to **04 Model Performance** to view real accuracy, F1-score, sensitivity, specificity, and confusion matrix visualizations.

---

## 🛡️ License & Safety Disclaimer

MediScope AI is provided under the MIT License for research and educational purposes.  
**MediScope AI does NOT provide medical diagnosis or treatment.** Always seek the advice of a qualified healthcare professional.
