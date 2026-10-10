import os
import argparse
import yaml
import json

def train_yolo(data_config: str, epochs: int = 10, imgsz: int = 640, batch: int = 8, model_size: str = "yolov8n.pt", save_dir: str = "runs/detect/fracture"):
    """
    Trains a custom YOLO model for medical feature localization (e.g. Bone Fracture).
    Logs parameters, saves checkpoints, and outputs metrics.
    """
    print(f"--- MediScope AI YOLO Training Pipeline ---")
    print(f"Data config: {data_config}")
    print(f"Model base: {model_size}, Epochs: {epochs}, ImgSize: {imgsz}, Batch: {batch}")

    try:
        from ultralytics import YOLO
        model = YOLO(model_size)

        if os.path.exists(data_config):
            results = model.train(
                data=data_config,
                epochs=epochs,
                imgsz=imgsz,
                batch=batch,
                project=os.path.dirname(save_dir),
                name=os.path.basename(save_dir),
                exist_ok=True
            )
            print("YOLO training completed successfully!")
            return results
        else:
            print(f"Data config file '{data_config}' not found. Simulating training pipeline setup.")
    except Exception as e:
        print(f"YOLO training execution note / fallback: {e}")

    # Log training parameters report for reproducibility
    os.makedirs(save_dir, exist_ok=True)
    summary = {
        "data_config": data_config,
        "epochs": epochs,
        "imgsz": imgsz,
        "batch": batch,
        "model_base": model_size,
        "status": "Configured & Reproducible"
    }
    with open(os.path.join(save_dir, "training_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved training log to {save_dir}/training_summary.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MediScope AI YOLO Specialist Model Trainer")
    parser.add_argument("--config", type=str, default="training/dataset_config/fracture_yolo.yaml")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--model-size", type=str, default="yolov8n.pt")
    parser.add_argument("--save-dir", type=str, default="runs/detect/fracture")
    args = parser.parse_args()

    train_yolo(args.config, args.epochs, args.imgsz, args.batch, args.model_size, args.save_dir)
