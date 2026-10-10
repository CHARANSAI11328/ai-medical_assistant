from PIL import Image
import io
from services.image_preprocessing import ImagePreprocessingService

def test_valid_image_preprocessing():
    img = Image.new("RGB", (200, 200), color=(100, 100, 100))
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    is_valid, processed_img, msg = ImagePreprocessingService.validate_and_load_image(buf.getvalue(), "test.png")
    assert is_valid is True
    assert processed_img is not None
    assert processed_img.width == 200
    assert processed_img.height == 200

def test_too_small_image():
    img = Image.new("RGB", (30, 30), color=(100, 100, 100))
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    is_valid, processed_img, msg = ImagePreprocessingService.validate_and_load_image(buf.getvalue(), "small.png")
    assert is_valid is False
    assert "too small" in msg

if __name__ == "__main__":
    test_valid_image_preprocessing()
    test_too_small_image()
    print("All Preprocessing Unit Tests Passed!")
