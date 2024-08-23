import os
import json
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model for object detection
model = YOLO('yolov8n.pt')

def detect_objects (master_id):
    # Initialize a list to store detection results
    detection_results = []

    segmented_dir = os.path.join('segmented_objects', master_id)
    
    # Iterate over all files in the segmented objects directory
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

            # Perform object detection
            results = model(img)

            # Collect detected object information
            detected_objects = []
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls)  # Class index
                    conf = box.conf  # Confidence score
                    label = model.names[cls]  # Convert class index to label

                    detected_objects.append({
                        'label': label,
                        'confidence': float(conf)
                    })

            # Save the detection result with the object ID and master ID
            detection_results.append({
                'object_id': object_id,
                'master_id': master_id,
                'detected_objects': detected_objects
            })
            
    output_json = os.path.join('json_files', master_id)
    
    if not os.path.exists(output_json):
        os.makedirs(output_json)
        
    output_json = os.path.join(output_json, 'detection_results.json')
        
    # Save the detection results to a JSON file
    with open(output_json, 'w') as f:
        json.dump(detection_results, f, indent=4)

    print(f"Object detection completed. Results saved in '{output_json}'.")

if __name__ == '__main__':
    detect_objects('1bc8c3e6-8ac3-4de5-8e83-068a82cd640e')
