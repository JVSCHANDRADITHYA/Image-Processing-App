from models.segmentation_model import segment_image
from models.identification_model import detect_objects
from models.summarization_model import generate_summary
from models.text_extraction_model import extract_text
from utils.preprocessing import load_image, preprocess_image
from utils.postprocessing import save_image
from utils.final_json import generate_final_json
from utils.create_table import generate_final_output
import cv2
import PIL
import numpy
import matplotlib.pyplot as plt

image_path = 'uploaded_images\input_image.webp'

master_id = segment_image(image_path)
print(master_id)
detect_objects(master_id)
extract_text(master_id)
generate_summary(master_id)

generate_final_json(master_id)
generate_final_output(master_id, image_path)


