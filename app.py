import streamlit as st
import cv2
import numpy as np
import os
import json
import uuid
import pandas as pd
from PIL import Image
from utils.preprocessing import preprocess_image
from utils.postprocessing import save_image, overlay_segmentation
from utils.data_mapping import load_metadata, map_data_to_objects
from utils.visualization import plot_image_with_boxes, generate_final_output
from models.segmentation_model import segment_image
from models.identification_model import detect_objects
from models.text_extraction_model import extract_text
from models.summarization_model import generate_summary

st.title("AI Pipeline for Image Segmentation and Object Analysis")

# Initialize session state for master_id
if 'master_id' not in st.session_state:
    st.session_state.master_id = None

# File uploader
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    # Save uploaded file
    input_image_path = 'uploaded_images/input_image.' + uploaded_file.name.split('.')[-1]
    with open(input_image_path, 'wb') as f:
        f.write(uploaded_file.read())

    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Step 1: Image Segmentation
    if st.button("Run Segmentation"):
        st.session_state.master_id = segment_image(input_image_path)
        st.success(f"Segmentation completed. Master ID: {st.session_state.master_id}")

        # Load segmented images for display
        segmented_dir = os.path.join('segmented_objects', st.session_state.master_id)
        segmented_images = [os.path.join(segmented_dir, f) for f in os.listdir(segmented_dir) if f.endswith('.png')]

        st.subheader("Segmented Objects")
        for img_path in segmented_images:
            st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)

    # Proceed only if master_id is available
    if st.session_state.master_id:
        # Step 2: Object Identification
        if st.button("Run Object Identification"):
            detect_objects(st.session_state.master_id)
            st.success("Object identification completed.")

        # Step 3: Text Extraction
        if st.button("Run Text Extraction"):
            extract_text(st.session_state.master_id)
            st.success("Text extraction completed.")

        # Step 4: Summarization
        if st.button("Run Summarization"):
            generate_summary(st.session_state.master_id)
            st.success("Summarization completed.")

        # Display results
        json_dir = os.path.join('json_files', st.session_state.master_id)
        detection_results_path = os.path.join(json_dir, 'detection_results.json')
        text_extraction_results_path = os.path.join(json_dir, 'text_extraction_results.json')
        summaries_path = os.path.join(json_dir, 'object_summaries.json')

        if os.path.exists(detection_results_path):
            with open(detection_results_path, 'r') as f:
                detection_results = json.load(f)

            if os.path.exists(text_extraction_results_path):
                with open(text_extraction_results_path, 'r') as f:
                    text_results = json.load(f)

            if os.path.exists(summaries_path):
                with open(summaries_path, 'r') as f:
                    summaries = json.load(f)

            # Display object details
            st.subheader("Object Details")
            for result in detection_results:
                object_id = result['object_id']
                st.write(f"Object ID: {object_id}")

                # Display detected objects
                for obj in result['detected_objects']:
                    st.write(f"Label: {obj['label']}, Confidence: {obj['confidence']:.2f}")

                # Display extracted text
                text_data = next((item['extracted_text'] for item in text_results if item['object_id'] == object_id), "")
                st.write(f"Extracted Text: {text_data}")

                # Display summary
                summary_data = next((item['summary'] for item in summaries if item['object_id'] == object_id), "")
                st.write(f"Summary: {summary_data}")

            # Prepare final output
            final_output_path = os.path.join('output', f"{st.session_state.master_id}_final_output.png")
            generate_final_output(input_image_path, detection_results, final_output_path)

            st.subheader("Final Output")
            st.image(final_output_path, caption="Final Output Image", use_column_width=True)

            # Display final table
            data_mapping = map_data_to_objects(detection_results, text_results)
            df = pd.DataFrame(data_mapping.values())
            st.write("Summary Table")
            st.dataframe(df)