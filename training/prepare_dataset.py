import os
import yaml
import json
import argparse
import random
from typing import Dict, Any, List

def create_sample_dataset_structure(output_dir: str = "datasets/sample_data"):
    """
    Creates reproducible dataset directory structure and sample dataset YAML configs.
    Ensures patient-level split isolation.
    """
    os.makedirs(os.path.join(output_dir, "fractures", "images", "train"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "fractures", "images", "val"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "fractures", "labels", "train"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "fractures", "labels", "val"), exist_ok=True)

    # Generate YOLO dataset configuration file
    yolo_config = {
        "path": os.path.abspath(os.path.join(output_dir, "fractures")),
        "train": "images/train",
        "val": "images/val",
        "names": {
            0: "Fracture Region",
            1: "Dislocation",
            2: "Bone Lesion"
        }
    }

    config_path = "training/dataset_config/fracture_yolo.yaml"
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(yolo_config, f)

    print(f"Generated YOLO dataset configuration at {config_path}")

def prepare_splits(data_items: List[Dict[str, Any]], train_ratio=0.7, val_ratio=0.15, seed=42):
    """
    Groups items by patient_id to prevent patient data leakage across splits.
    """
    random.seed(seed)
    patient_groups = {}
    for item in data_items:
        pid = item.get("patient_id", item.get("filename"))
        patient_groups.setdefault(pid, []).append(item)

    patients = list(patient_groups.keys())
    random.shuffle(patients)

    n_patients = len(patients)
    n_train = int(n_patients * train_ratio)
    n_val = int(n_patients * val_ratio)

    train_patients = set(patients[:n_train])
    val_patients = set(patients[n_train:n_train + n_val])
    test_patients = set(patients[n_train + n_val:])

    train_data, val_data, test_data = [], [], []
    for pid, items in patient_groups.items():
        if pid in train_patients:
            train_data.extend(items)
        elif pid in val_patients:
            val_data.extend(items)
        else:
            test_data.extend(items)

    return train_data, val_data, test_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MediScope AI Dataset Preparation Tool")
    parser.add_argument("--output-dir", type=str, default="datasets/sample_data")
    args = parser.parse_args()

    create_sample_dataset_structure(args.output_dir)
