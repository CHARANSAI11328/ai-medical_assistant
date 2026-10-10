import io
from typing import Tuple, Dict, Any, Optional
from PIL import Image, ImageOps
import numpy as np

class ImagePreprocessingService:
    """
    Robust medical image validation, EXIF metadata stripping, 
    and format normalization.
    """
    MAX_FILE_SIZE_MB = 15.0
    MAX_DIMENSION = 4096
    MIN_DIMENSION = 64

    @staticmethod
    def validate_and_load_image(file_bytes: bytes, filename: str) -> Tuple[bool, Optional[Image.Image], str]:
        """
        Validates file size, decodes image, corrects orientation, strips EXIF, 
        and verifies dimensions.
        Returns: (is_valid: bool, image: Optional[PIL.Image], error_or_success_message: str)
        """
        size_mb = len(file_bytes) / (1024 * 1024)
        if size_mb > ImagePreprocessingService.MAX_FILE_SIZE_MB:
            return False, None, f"File size ({size_mb:.1f} MB) exceeds maximum limit of {ImagePreprocessingService.MAX_FILE_SIZE_MB} MB."

        try:
            img = Image.open(io.BytesIO(file_bytes))
            img.verify()  # Verify integrity
            img = Image.open(io.BytesIO(file_bytes))  # Re-open after verify
        except Exception as e:
            return False, None, f"Failed to decode image file '{filename}': {str(e)}"

        # Correct orientation via EXIF if present
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

        w, h = img.size
        if w < ImagePreprocessingService.MIN_DIMENSION or h < ImagePreprocessingService.MIN_DIMENSION:
            return False, None, f"Image dimensions ({w}x{h}) are too small. Minimum required is {ImagePreprocessingService.MIN_DIMENSION}x{ImagePreprocessingService.MIN_DIMENSION} pixels."

        # Convert to RGB (handles RGBA, Palette, Grayscale, etc.)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Resize if dimensions exceed max
        if w > ImagePreprocessingService.MAX_DIMENSION or h > ImagePreprocessingService.MAX_DIMENSION:
            img.thumbnail((ImagePreprocessingService.MAX_DIMENSION, ImagePreprocessingService.MAX_DIMENSION), Image.Resampling.LANCZOS)

        return True, img, f"Image successfully validated ({img.width}x{img.height} px, RGB)."

    @staticmethod
    def prepare_for_model(img: Image.Image, target_size: Tuple[int, int] = (224, 224)) -> Image.Image:
        """Prepares image by resizing to target input shape."""
        return img.resize(target_size, Image.Resampling.LANCZOS)
