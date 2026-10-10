import numpy as np
try:
    import cv2
except Exception:
    cv2 = None
from PIL import Image
from typing import Tuple, Optional

try:
    import torch
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False

class SimpleGradCAM:
    """
    Lightweight Grad-CAM / Activation Map Generator for PyTorch models.
    Produces attribution maps highlighting visual regions that influenced predictions.
    """
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        if TORCH_AVAILABLE and hasattr(self.target_layer, 'register_forward_hook'):
            try:
                self.target_layer.register_forward_hook(self._save_activation)
                self.target_layer.register_full_backward_hook(self._save_gradient)
            except Exception:
                pass

    def _save_activation(self, module, input, output):
        self.activations = output

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate_heatmap(self, input_tensor, class_idx: Optional[int] = None) -> np.ndarray:
        if not TORCH_AVAILABLE or self.model is None:
            return np.zeros((224, 224), dtype=np.float32)

        try:
            self.model.eval()
            output = self.model(input_tensor)
            
            if class_idx is None:
                class_idx = output.argmax(dim=1).item()

            self.model.zero_grad()
            target_score = output[0, class_idx]
            target_score.backward(retain_graph=True)

            if self.gradients is None or self.activations is None:
                return np.zeros((224, 224), dtype=np.float32)

            gradients = self.gradients.data.cpu().numpy()[0]
            activations = self.activations.data.cpu().numpy()[0]

            weights = np.mean(gradients, axis=(1, 2))
            cam = np.zeros(activations.shape[1:], dtype=np.float32)

            for i, w in enumerate(weights):
                cam += w * activations[i]

            cam = np.maximum(cam, 0)
            if np.max(cam) > 0:
                cam = cam / np.max(cam)
            return cam
        except Exception:
            return np.zeros((224, 224), dtype=np.float32)

def overlay_heatmap(orig_img: Image.Image, heatmap: np.ndarray, alpha: float = 0.4) -> Image.Image:
    """Overlays a 2D float heatmap (0 to 1) onto PIL Image."""
    orig_np = np.array(orig_img.convert("RGB"))
    h, w, _ = orig_np.shape
    
    resized_cam = cv2.resize(heatmap, (w, h))
    heatmap_colored = cv2.applyColorMap(np.uint8(255 * resized_cam), cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    
    overlayed = (alpha * heatmap_colored + (1 - alpha) * orig_np).astype(np.uint8)
    return Image.fromarray(overlayed)
