import streamlit as st
from models.segmentation_model import segment_image
from models.identification_model import detect_objects
from models.text_extraction_model import extract_text
from models.summarization_model import summarize_object_attributes
import os
import json
from PIL import Image

# Path configuration
SEGMENTED_DIR = 'segmented_objects'
OUTPUT_JSON_DIR = '.'

# Helper function to save JSON data
def save_json(data, filename):
    with open(os.path.join(OUTPUT_JSON_DIR, filename), 'w') as f:
        json.dump(data, f, indent=4)

# Streamlit App Layout
st.title("Image Segmentation and Analysis App")

# Step 1: Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "webp"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    if not os.path.exists('uploaded_images'):
        os.makedirs('uploaded_images')
    
    # Save uploaded image
    input_image_path = os.path.join("uploaded_images", uploaded_file.name)
    image.save(input_image_path)

    st.write("Image uploaded successfully!")

    # Step 2: Segment Image
    if st.button('Segment Image'):
        segment_image(input_image_path, SEGMENTED_DIR)
        st.write(f"Segmentation completed. Segmented images are saved in '{SEGMENTED_DIR}'.")

        # Display segmented images
        segmented_images = [os.path.join(SEGMENTED_DIR, f) for f in os.listdir(SEGMENTED_DIR) if f.endswith('.png')]
        for img_path in segmented_images:
            img = Image.open(img_path)
            st.image(img, caption=f'Segmented Image: {os.path.basename(img_path)}', use_column_width=True)

    # Step 3: Perform Object Detection
    if st.button('Detect Objects'):
        detection_results = detect_objects(SEGMENTED_DIR, 'detection_results.json')
        save_json(detection_results, 'detection_results.json')
        st.write("Object detection completed. Results saved in 'detection_results.json'.")

    # Step 4: Extract Text
    if st.button('Extract Text'):
        text_results = extract_text(SEGMENTED_DIR, 'text_extraction_results.json')
        save_json(text_results, 'text_extraction_results.json')
        st.write("Text extraction completed. Results saved in 'text_extraction_results.json'.")

    # Step 5: Summarize Object Attributes
    if st.button('Summarize Attributes'):
        detection_results = json.load(open(os.path.join(OUTPUT_JSON_DIR, 'detection_results.json')))
        text_results = json.load(open(os.path.join(OUTPUT_JSON_DIR, 'text_extraction_results.json')))
        summaries = summarize_object_attributes(detection_results, text_results)
        save_json(summaries, 'object_summaries.json')
        st.write("Summarization completed. Results saved in 'object_summaries.json'.")

        # Display the summary for each object
        for summary in summaries:
            st.write(f"Object ID: {summary['object_id']}")
            st.write(f"Summary: {summary['summary']}")
            st.write("---")

