import os
import json
import cv2
import easyocr

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify the languages

def extract_text(master_id):
    text_results = []

    segmented_dir = os.path.join('segmented_objects', master_id)
    
    for filename in os.listdir(segmented_dir):
        if filename.endswith('.png'):
            object_image_path = os.path.join(segmented_dir, filename)
            
            # Extract object ID and master ID from the filename
            parts = filename.split('_')
            object_id = parts[1].split('.')[0]

            # Load the segmented object image
            img = cv2.imread(object_image_path)
            if img is None:
                print(f"Error: Unable to load image '{object_image_path}'.")
                continue

            # Perform text extraction using EasyOCR
            result = reader.readtext(img)

            # Extract detected text
            extracted_text = " ".join([text for _, text, _ in result])

            # Save the text extraction result with the object ID and master ID
            text_results.append({
                'object_id': object_id,
                'master_id': master_id,
                'extracted_text': extracted_text
            })

    output_json = os.path.join('json_files', master_id)
    
    if not os.path.exists(output_json):
        os.makedirs(output_json)
    
    output_json = os.path.join(output_json, 'text_extraction_results.json')
    
    # Save the text extraction results to a JSON file
    with open(output_json, 'w') as f:
        json.dump(text_results, f, indent=4)

    print(f"Text extraction completed. Results saved in '{output_json}'.")

# Example usage
if __name__ == '__main__':
    extract_text('f6448034-5911-4791-ac7f-bb8853ac4252')
