from PIL import Image
from models.registry import ModelRegistry

def test_model_registry_instantiation():
    registry = ModelRegistry()
    specialists = registry.list_specialists()
    assert len(specialists) >= 4

def test_eye_specialist_prediction():
    registry = ModelRegistry()
    eye_model = registry.get_specialist("eye")
    assert eye_model is not None
    
    img = Image.new("RGB", (224, 224), color=(180, 50, 20))
    prediction = eye_model.predict(img)
    
    assert prediction.specialist_key == "eye"
    assert prediction.predicted_label is not None
    assert prediction.confidence > 0.0

def test_fracture_yolo_prediction():
    registry = ModelRegistry()
    fracture_model = registry.get_specialist("fracture")
    assert fracture_model is not None

    img = Image.new("RGB", (200, 300), color=(50, 50, 50))
    prediction = fracture_model.predict(img)

    assert prediction.specialist_key == "fracture"
    assert prediction.task_type == "detection"
    assert prediction.visual_explanation_image is not None

if __name__ == "__main__":
    test_model_registry_instantiation()
    test_eye_specialist_prediction()
    test_fracture_yolo_prediction()
    print("All Model Unit Tests Passed!")
