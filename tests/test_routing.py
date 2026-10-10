from PIL import Image
from models.router import SpecialistRouter

def test_explicit_routing():
    router = SpecialistRouter()
    img = Image.new("RGB", (200, 200), color=(100, 100, 100))
    success, specialist, msg = router.route_image(img, user_selected_modality="chest")
    
    assert success is True
    assert specialist is not None
    assert specialist.key == "chest"

def test_invalid_modality_routing():
    router = SpecialistRouter()
    img = Image.new("RGB", (200, 200), color=(100, 100, 100))
    success, specialist, msg = router.route_image(img, user_selected_modality="invalid_specialty")
    
    assert success is False
    assert specialist is None

if __name__ == "__main__":
    test_explicit_routing()
    test_invalid_modality_routing()
    print("All Routing Unit Tests Passed!")
