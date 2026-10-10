from typing import Tuple, Optional, Dict, Any
from PIL import Image
import numpy as np
try:
    import cv2
except Exception:
    cv2 = None
from models.registry import ModelRegistry
from models.base_model import BaseSpecialistModel

class SpecialistRouter:
    """
    Routing engine that validates input image suitability and assigns the appropriate 
    specialist model adapter based on explicit selection or automated image analysis.
    """
    def __init__(self):
        self.registry = ModelRegistry()

    def route_image(
        self,
        image: Image.Image,
        user_selected_modality: Optional[str] = None
    ) -> Tuple[bool, Optional[BaseSpecialistModel], str]:
        """
        Routes image to appropriate specialist model.
        Returns: (success: bool, specialist_model: Optional[BaseSpecialistModel], message: str)
        """
        # 1. Explicit user selection priority
        if user_selected_modality and user_selected_modality.lower() != "auto":
            key = user_selected_modality.lower()
            specialist = self.registry.get_specialist(key)
            if specialist:
                return True, specialist, f"Routed to explicit specialty: {specialist.name}"
            else:
                return False, None, f"Selected modality '{user_selected_modality}' is not configured."

        # 2. Automatic Modality Routing Analysis
        img_np = np.array(image.convert("RGB"))
        h, w, c = img_np.shape

        # Check grayscale / radiograph characteristics (R, G, B channels nearly equal)
        diff_rg = np.mean(np.abs(img_np[:, :, 0].astype(int) - img_np[:, :, 1].astype(int)))
        diff_gb = np.mean(np.abs(img_np[:, :, 1].astype(int) - img_np[:, :, 2].astype(int)))
        is_grayscale_like = (diff_rg < 12.0) and (diff_gb < 12.0)

        if is_grayscale_like:
            # Distinguish Chest X-Ray vs Bone Fracture X-Ray by aspect ratio & central density
            aspect_ratio = w / float(h)
            if 0.75 <= aspect_ratio <= 1.35:
                specialist = self.registry.get_specialist("chest")
                return True, specialist, "Automatically identified Chest Radiograph (X-Ray)."
            else:
                specialist = self.registry.get_specialist("fracture")
                return True, specialist, "Automatically identified Limb / Bone Radiograph."

        # Check Retinal Fundus (Strong central red saturation)
        mean_red = np.mean(img_np[:, :, 0])
        mean_green = np.mean(img_np[:, :, 1])
        if mean_red > mean_green * 1.3 and mean_red > 80:
            specialist = self.registry.get_specialist("eye")
            return True, specialist, "Automatically identified Retinal Fundus Photograph."

        # Check Plant Leaf (Strong green channel dominance)
        mean_blue = np.mean(img_np[:, :, 2])
        if mean_green > mean_red * 1.1 and mean_green > mean_blue * 1.1:
            specialist = self.registry.get_specialist("agriculture")
            return True, specialist, "Automatically identified Agricultural Crop Leaf."

        # Fallback / Ambiguous Modality
        return False, None, (
            "Could not automatically determine image modality with high confidence. "
            "Please explicitly select the medical specialty above."
        )
