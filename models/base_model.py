from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import numpy as np
from PIL import Image

@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    label: str

@dataclass
class SpecialistPrediction:
    specialist_key: str
    specialist_name: str
    modality: str
    task_type: str  # 'classification' or 'detection'
    predicted_label: str
    confidence: float
    all_class_probabilities: Dict[str, float] = field(default_factory=dict)
    bounding_boxes: List[BoundingBox] = field(default_factory=list)
    visual_explanation_image: Optional[Image.Image] = None  # Annotated image or Grad-CAM
    visual_explanation_type: str = "none"  # 'bounding_box', 'gradcam', 'none'
    uncertainty_note: str = ""
    is_demo: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

class BaseSpecialistModel(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.key = config.get("modality_key", "unknown")
        self.name = config.get("name", "Specialist Model")
        self.modality = config.get("modality", "Medical Image")
        self.task_type = config.get("task_type", "classification")
        self.weight_path = config.get("weight_path", "")
        self.confidence_threshold = config.get("confidence_threshold", 0.5)
        self.labels = config.get("labels", {})
        self.is_loaded = False
        self.is_demo_mode = False

    @abstractmethod
    def load_model(self) -> bool:
        """Load model weights or fallback to validated baseline demo mode."""
        pass

    @abstractmethod
    def preprocess(self, image: Image.Image) -> Any:
        """Preprocess PIL image into model-ready format."""
        pass

    @abstractmethod
    def predict(self, image: Image.Image) -> SpecialistPrediction:
        """Perform model inference and return standardized SpecialistPrediction."""
        pass
