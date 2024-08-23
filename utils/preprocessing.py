import cv2
import numpy as np
from PIL import Image

def load_image(image_path):
    """Load an image from file path."""
    image = Image.open(image_path).convert('RGB')
    return np.array(image)

def resize_image(image, size=(256, 256)):
    """Resize image to the specified size."""
    return cv2.resize(image, size, interpolation=cv2.INTER_LINEAR)

def normalize_image(image):
    """Normalize image to the range [0, 1]."""
    return image / 255.0

def preprocess_image(image_path, size=(256, 256)):
    """Load, resize, and normalize image."""
    image = load_image(image_path)
    image = resize_image(image, size)
    image = normalize_image(image)
    return image
