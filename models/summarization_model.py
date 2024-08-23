import json
import os

def generate_summary(master_id):
    # Load detection results from JSON file
    
    input_json = os.path.join('json_files', master_id, 'detection_results.json')
    
    with open(input_json, 'r') as f:
        detection_results = json.load(f)

    # Initialize a list to store summaries
    summaries = []

    for result in detection_results:
        object_id = result['object_id']
        master_id = result['master_id']
        detected_objects = result['detected_objects']

        # Generate summary for detected objects
        object_descriptions = []
        for obj in detected_objects:
            label = obj['label']
            confidence = obj['confidence']
            object_description = f"A {label} was detected with a confidence score of {confidence:.2f}."
            object_descriptions.append(object_description)

        if len(object_descriptions) == 0:
            summary_text = "DESCRIPTION NOT AVAILABLE FOR THE OBJECT"
        else :
            # Combine descriptions
            summary_text = " ".join(object_descriptions)
        
        # Add metadata to the summary
        summary = {
            'object_id': object_id,
            'master_id': master_id,
            'summary': summary_text
        }
        
        summaries.append(summary)

    # Ensure the output directory exists
    output_json = os.path.join('json_files', master_id)
    
    if not os.path.exists(output_json):
        os.makedirs(output_json)
    
    output_json = os.path.join(output_json, 'object_summaries.json')

    # Save the summaries to a JSON file
    with open(output_json, 'w') as f:
        json.dump(summaries, f, indent=4)

    print(f"Summaries generated and saved in '{output_json}'.")

# Example usage
if __name__ == '__main__':
    generate_summary('1bc8c3e6-8ac3-4de5-8e83-068a82cd640e')