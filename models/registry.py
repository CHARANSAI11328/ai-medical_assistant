import os
import yaml
from typing import Dict, Any, List, Optional
from models.base_model import BaseSpecialistModel
from models.eye_specialist import EyeSpecialistModel
from models.chest_specialist import ChestSpecialistModel
from models.fracture_specialist import FractureSpecialistModel
from models.agriculture_specialist import AgricultureSpecialistModel

class ModelRegistry:
    """
    Central registry that loads specialist model configurations and maintains singletons.
    """
    _instance = None

    def __new__(cls, config_path: str = "configs/models.yaml"):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
            cls._instance._init_registry(config_path)
        return cls._instance

    def _init_registry(self, config_path: str):
        self.specialists: Dict[str, BaseSpecialistModel] = {}
        self.configs: Dict[str, Any] = {}

        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self.configs = data.get("models", {})

        # Instantiate specialist adapters
        if "eye_specialist" in self.configs:
            self.specialists["eye"] = EyeSpecialistModel(self.configs["eye_specialist"])
        if "chest_specialist" in self.configs:
            self.specialists["chest"] = ChestSpecialistModel(self.configs["chest_specialist"])
        if "fracture_specialist" in self.configs:
            self.specialists["fracture"] = FractureSpecialistModel(self.configs["fracture_specialist"])
        if "agriculture_specialist" in self.configs:
            self.specialists["agriculture"] = AgricultureSpecialistModel(self.configs["agriculture_specialist"])

    def get_specialist(self, key: str) -> Optional[BaseSpecialistModel]:
        return self.specialists.get(key.lower())

    def list_specialists(self) -> List[Dict[str, Any]]:
        result = []
        for k, spec in self.specialists.items():
            result.append({
                "key": k,
                "name": spec.name,
                "modality": spec.modality,
                "task_type": spec.task_type,
                "confidence_threshold": spec.confidence_threshold,
                "is_demo_mode": spec.is_demo_mode
            })
        return result
