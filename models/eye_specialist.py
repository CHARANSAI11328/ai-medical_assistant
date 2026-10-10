import os
from PIL import Image
import numpy as np
import cv2
from typing import Dict, Any, Tuple
from models.base_model import BaseSpecialistModel, SpecialistPrediction
from models.gradcam import overlay_heatmap

try:
    import torch
    import torch.nn as nn
    import torchvision.transforms as T
    from torchvision.models import resnet50
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False

class EyeSpecialistModel(BaseSpecialistModel):
    """
    Specialist Computer Vision model for Ocular & Retinal Fundus Image Analysis.
    Analyzes retinal photography for Diabetic Retinopathy, Glaucoma, Cataracts, and AMD.
    """
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") if TORCH_AVAILABLE else "cpu"
        self.model = None

    def load_model(self) -> bool:
        if TORCH_AVAILABLE and self.weight_path and os.path.exists(self.weight_path):
            try:
                self.model = resnet50(pretrained=False)
                num_ftrs = self.model.fc.in_features
                self.model.fc = nn.Linear(num_ftrs, len(self.labels))
                
                checkpoint = torch.load(self.weight_path, map_location=self.device)
                self.model.load_state_dict(checkpoint)
                self.model.to(self.device)
                self.model.eval()
                self.is_loaded = True
                self.is_demo_mode = False
                return True
            except Exception as e:
                print(f"Failed to load eye specialist weights: {e}")

        self.is_loaded = True
        self.is_demo_mode = True
        return True

    def preprocess(self, image: Image.Image):
        if TORCH_AVAILABLE:
            transform = T.Compose([
                T.Resize((224, 224)),
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            return transform(image).unsqueeze(0).to(self.device)
        return image

    def predict(self, image: Image.Image) -> SpecialistPrediction:
        if not self.is_loaded:
            self.load_model()

        if TORCH_AVAILABLE and self.model is not None and not self.is_demo_mode:
            input_tensor = self.preprocess(image)
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probs = torch.softmax(outputs, dim=1)[0].cpu().numpy()
            
            top_class = int(np.argmax(probs))
            confidence = float(probs[top_class])
            predicted_label = self.labels.get(top_class, f"Class {top_class}")
            class_probs = {self.labels.get(i, f"Class {i}"): float(probs[i]) for i in range(len(probs))}

            return SpecialistPrediction(
                specialist_key=self.key,
                specialist_name=self.name,
                modality=self.modality,
                task_type=self.task_type,
                predicted_label=predicted_label,
                confidence=confidence,
                all_class_probabilities=class_probs,
                visual_explanation_image=image,
                visual_explanation_type="gradcam",
                uncertainty_note=f"ResNet-50 fundus model active. Confidence: {confidence*100:.1f}%.",
                is_demo=False
            )
        else:
            # Deterministic baseline analysis for demo mode
            img_np = np.array(image.convert("RGB"))
            avg_red = float(np.mean(img_np[:, :, 0]))

            if avg_red > 140:
                top_class = 1  # Diabetic Retinopathy Signs
            elif avg_red > 100:
                top_class = 2  # Glaucoma Signs
            else:
                top_class = 0  # Normal Retinal

            predicted_label = self.labels.get(top_class, "Normal Retinal Finding")
            class_probs = {
                self.labels.get(0, "Normal"): 0.91 if top_class == 0 else 0.12,
                self.labels.get(1, "DR"): 0.84 if top_class == 1 else 0.08,
                self.labels.get(2, "Glaucoma"): 0.76 if top_class == 2 else 0.05,
                self.labels.get(3, "Cataract"): 0.03,
                self.labels.get(4, "AMD"): 0.02
            }
            total_p = sum(class_probs.values())
            class_probs = {k: v/total_p for k, v in class_probs.items()}
            confidence = class_probs[predicted_label]

            # Generate simulated Grad-CAM heatmap over optic disc region
            h, w, _ = img_np.shape
            synthetic_cam = np.zeros((h, w), dtype=np.float32)
            cv2.circle(synthetic_cam, (int(w * 0.6), int(h * 0.5)), int(min(w, h) * 0.25), 1.0, -1)
            synthetic_cam = cv2.GaussianBlur(synthetic_cam, (51, 51), 0)
            gradcam_img = overlay_heatmap(image, synthetic_cam)

            return SpecialistPrediction(
                specialist_key=self.key,
                specialist_name=self.name,
                modality=self.modality,
                task_type=self.task_type,
                predicted_label=predicted_label,
                confidence=confidence,
                all_class_probabilities=class_probs,
                visual_explanation_image=gradcam_img,
                visual_explanation_type="gradcam",
                uncertainty_note="Demo Baseline Evaluation Mode. Simulated optic disc & macula feature extraction.",
                is_demo=True
            )
