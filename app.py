import streamlit as st
from models.segmentation_model import segment_image
from models.identification_model import detect_objects
from models.summarization_model import generate_summary
from models.text_extraction_model import extract_text
from utils.final_json import generate_final_json
from utils.create_table import generate_final_output
import os
import shutil
import base64

# Function to encode local image as base64
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load your local background image
img = get_img_as_base64("resources/bg_image.jpg")  # Replace with your image path

# Custom CSS for a more colorful and appealing design with a background image
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
background-repeat: no-repeat;
# background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,255,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
h1 {{
    font-size: 5em;
    font-weight: bold;
    color:#FFC0CB;
    font-family: 'Courier New', monospace;
    text-align: left;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def process_image(image_path):
    st.write("### Processing Image...")
    master_id = segment_image(image_path)
    st.write('### MASTER ID OF THE IMAGE ')
    st.markdown(f"<h2 style='text-align: center; color: blue;'>{master_id}</h2>", unsafe_allow_html=True)
    
    st.write("### Detecting Objects...")
    detect_objects(master_id)
    
    st.write("### Extracting Text...")
    extract_text(master_id)
    
    st.write("### Generating Summary...")
    generate_summary(master_id)
    
    st.write("### Generating Final JSON...")
    generate_final_json(master_id)
    
    st.write("### Creating Final Output...")
    generate_final_output(master_id, image_path)
    
    return master_id

def display_output(master_id, image_path):
    output_dir = os.path.join('final_outputs', master_id)
    final_output_path = os.path.join(output_dir, 'final_output.png')
    
    st.write("### Final Output")
    st.image(final_output_path, caption="Final Output with Annotated Image and Summary Table", use_column_width=True)
    
    # Download options
    st.write("### Download Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with open(image_path, "rb") as file:
            btn = st.download_button(
                label="Download Original Image",
                data=file,
                file_name=os.path.basename(image_path),
                mime="image/png"
            )
    
    with col2:
        with open(final_output_path, "rb") as file:
            btn = st.download_button(
                label="Download Final Output",
                data=file,
                file_name=f"{master_id}_final_output.png",
                mime="image/png"
            )
    
    table_path = os.path.join(output_dir, 'summary_table.png')
    with col3:
        with open(table_path, "rb") as file:
            btn = st.download_button(
                label="Download Summary Table",
                data=file,
                file_name=f"{master_id}_summary_table.png",
                mime="image/png"
            )

def export_results(master_id):
    segmented_dir = os.path.join('segmented_objects', master_id)
    json_dir = os.path.join('json_files', master_id)
    results_dir = os.path.join('results', master_id)
    
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Copy segmented objects
    segmented_results_dir = os.path.join(results_dir, 'segmented_objects')
    shutil.copytree(segmented_dir, segmented_results_dir)
    
    # Copy JSON files
    json_results_dir = os.path.join(results_dir, 'json_files')
    shutil.copytree(json_dir, json_results_dir)
    
    st.write(f"### Results exported to '{results_dir}'")

def main():
    st.title("AI Image Processing Pipeline")  # Main title with styles applied
    st.write("This app processes an image through a pipeline that includes segmentation, object detection, text extraction, summarization, and final output generation.")
    
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        image_path = os.path.join("uploaded_images", uploaded_file.name)
        
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(image_path, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Process Image"):
            master_id = process_image(image_path)
            display_output(master_id, image_path)
            export_results(master_id)
    
    st.markdown("""
    <hr>
    <center>
    <span style='color: #FFC0CB; font-size: 20px; font-family: Courier New, sans-serif; font-weight: bold;'>
    Made with and for WASSERSTOFF
    </span>
    </center>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
