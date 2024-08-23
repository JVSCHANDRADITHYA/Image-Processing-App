import numpy as np
import cv2

def denormalize_image(image):
    """Convert image from [0, 1] range back to [0, 255]."""
    return (image * 255).astype(np.uint8)

def save_image(image, save_path):
    """Save image to the specified file path."""
    image = denormalize_image(image)
    cv2.imwrite(save_path, image)

def overlay_segmentation(image, masks, color=(0, 255, 0), alpha=0.5):
    """Overlay segmentation masks on the original image."""
    overlay = image.copy()
    for mask in masks:
        overlay[mask] = np.where(overlay[mask] == 0, color, overlay[mask])
    return cv2.addWeighted(image, alpha, overlay, 1 - alpha, 0)
