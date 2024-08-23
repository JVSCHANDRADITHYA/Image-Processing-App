# v-s-chandradithya-wasserstoff-AiInternTask
 
# AI Image Processing Pipeline

## Overview

This project involves developing a comprehensive AI pipeline for image segmentation and object analysis. The pipeline processes an input image to segment, identify, and analyze objects within it, and outputs a summary table with mapped data for each object. The application includes a Streamlit UI for interactive testing and visualization of results.

## Project Structure

1. **Image Segmentation**: Segment objects within an input image using a model such as Mask R-CNN or DETR.
2. **Object Extraction and Storage**: Extract segmented objects, assign unique IDs, and save them with metadata.
3. **Object Identification**: Identify each object using models like YOLO, Faster R-CNN, or CLIP and generate descriptions.
4. **Text/Data Extraction**: Extract text or data from object images using OCR tools like Tesseract OCR or EasyOCR.
5. **Summarize Object Attributes**: Summarize attributes of each object using NLP models and summarization algorithms.
6. **Data Mapping**: Map all extracted data and attributes to each object and the master image.
7. **Output Generation**: Generate a final output image with annotations and a summary table.

## Setup Instructions

### Prerequisites

- Python 3.x
- Required Python libraries (e.g., TensorFlow, PyTorch, OpenCV, PIL, Streamlit, etc.)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/JVSCHANDRADITHYA/v-s-chandradithya-wasserstoff-AiInternTask.git
    cd v-s-chandradithya-wasserstoff-AiInternTask
    ```

2. Install miniconda or anaconda if you haven't:
    ```bash
    conda env create -f environment.yml
    conda activate task
    ```

3. Run the main.py file for a cmdline implmentation 
    ```bash
    python main.py
    ```
    If you run it for the first time `yolox-seg.pt` would be installed on your device. All process would be initiated and json files would be in your home directory in `json_files` and segmented images can be found in `segmented_objects`

## Usage

1. **Start the Streamlit App**:
    ```bash
    streamlit run app.py
    ```

2. **Upload an Image**:
    - Use the Streamlit UI to upload an image.

3. **Process the Image**:
    - Click the "Process Image" button to run the image through the pipeline.

4. **View Results**:
    - The processed image with segmented objects and the summary table will be displayed.
    - Download options for the original image, final output, and summary table are available.

5. **Export Results**:
    - Use the export functionality to save segmented objects and metadata.


## Documentation

- **Code Documentation**: Detailed comments and explanations are provided within the code.
- **User Documentation**: This README.md file provides an overview and instructions for setup and usage.

## Presentation

A presentation summarizing the approach, implementation, results, and challenges faced is included in the project folder. It consists of 3-5 slides.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or feedback, please contact:

- **Name**: CHANDRADITHYA JANASWAMI
- **Email**: adithya.jvsc@gmail.com
