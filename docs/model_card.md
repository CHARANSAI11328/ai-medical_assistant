# MediScope AI Model Cards

## 1. Ocular & Retinal Specialist Model
- **Architecture:** ResNet-50 PyTorch Classifier + Grad-CAM Heatmap Layer.
- **Input:** 224x224 RGB image (Normalized with ImageNet statistics).
- **Output:** Multiclass probability distribution over 5 retinal findings.
- **Explainability:** SimpleGradCAM on `layer4[-1]`.

## 2. Chest Radiograph Specialist Model
- **Architecture:** DenseNet-121 PyTorch Classifier + Grad-CAM Layer.
- **Input:** 224x224 RGB/Grayscale Radiograph.
- **Output:** Pulmonary finding probabilities.
- **Explainability:** Grad-CAM on DenseBlock4.

## 3. Bone Fracture Specialist Model
- **Architecture:** YOLOv8 Small Object Detection Network.
- **Input:** 640x640 Image.
- **Output:** Bounding box coordinates `[x1, y1, x2, y2]`, confidence score, class label.
- **Explainability:** Native model-predicted bounding boxes.

## 4. Agricultural Crop Disease Specialist
- **Architecture:** MobileNetV3 Small PyTorch Classifier.
- **Input:** 224x224 Leaf Image.
- **Output:** Crop foliar status probabilities.
