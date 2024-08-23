import cv2
import numpy as np
from ultralytics import YOLO
import os
import uuid

# segments image and returns the master id for it
def segment_image(image_path):
    
    model = YOLO('yolov8x-seg.pt')
    
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found or unable to load.")
        return

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform segmentation
    results = model(img_rgb)

    # Unique ID for the original image
    master_id = str(uuid.uuid4())
    
    output_dir = os.path.join('segmented_objects', master_id)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare to save segmented objects
    segmented_objects = []

    # Iterate over results and save each segmented object
    for idx, result in enumerate(results):

        masks = result.masks
        if masks is not None:
            for i, mask in enumerate(masks.xy):
                # Create a blank image to store the segmented object
                mask_img = np.zeros_like(img_rgb)
                cv2.fillPoly(mask_img, [np.array(mask, dtype=np.int32)], (255, 255, 255))

                # Extract the object
                object_img = cv2.bitwise_and(img_rgb, mask_img)
                
                # Generate a unique ID for the object
                object_id = str(uuid.uuid4())

                # Save the object image
                object_image_path = os.path.join(output_dir, f"{master_id}_{object_id}.png")
                cv2.imwrite(object_image_path, cv2.cvtColor(object_img, cv2.COLOR_RGB2BGR))

                # Append metadata
                segmented_objects.append({
                    'object_id': object_id,
                    'master_id': master_id,
                    'object_image_path': object_image_path
                })

    # Save metadata
    metadata_path = os.path.join(output_dir, f"{master_id}_metadata.json")
    with open(metadata_path, 'w') as f:
        import json
        json.dump(segmented_objects, f, indent=4)

    print(f"Segmentation completed. Results saved in '{output_dir}'.")
    
    return master_id

#EXAMPLE USAGE
if __name__ == '__main__' :
    segment_image('uploaded_images\hqdefault.webp')
