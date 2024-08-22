import cv2
import numpy as np
from PIL import Image

def preprocess_image(image_file):
    # Convert the uploaded file to an OpenCV image
    image = Image.open(image_file)
    image = np.array(image)
    # Convert RGB to BGR which OpenCV uses
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    return image
