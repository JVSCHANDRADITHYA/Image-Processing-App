import os
import json

def generate_final_json(master_id):
    # Define paths to the three JSON files
    base_dir = os.path.join('json_files', master_id)
    detection_file = os.path.join(base_dir, 'detection_results.json')
    text_extraction_file = os.path.join(base_dir, 'text_extraction_results.json')
    summary_file = os.path.join(base_dir, 'object_summaries.json')
    
    # Load the contents of the JSON files
    with open(detection_file, 'r') as f:
        detection_results = json.load(f)
        
    with open(text_extraction_file, 'r') as f:
        text_extraction_results = json.load(f)
        
    with open(summary_file, 'r') as f:
        summaries = json.load(f)
    
    # Combine the data based on object_id and master_id
    final_data = []
    for detection in detection_results:
        object_id = detection['object_id']
        
        # Find corresponding text extraction result
        text_result = next((text for text in text_extraction_results if text['object_id'] == object_id), {})
        
        # Find corresponding summary result
        summary_result = next((summary for summary in summaries if summary['object_id'] == object_id), {})
        
        # Combine all data into one entry
        combined_entry = {
            'object_id': object_id,
            'master_id': detection['master_id'],
            'detected_objects': detection.get('detected_objects', []),
            'extracted_text': text_result.get('extracted_text', "TEXT NOT AVAILABLE"),
            'summary': summary_result.get('summary', "SUMMARY NOT AVAILABLE")
        }
        
        final_data.append(combined_entry)
    
    # Define the output path for the final JSON file
    final_json_path = os.path.join(base_dir, 'final_results.json')
    
    # Save the combined data into the final JSON file
    with open(final_json_path, 'w') as f:
        json.dump(final_data, f, indent=4)
    
    print(f"Final JSON file generated and saved in '{final_json_path}'.")

# Example usage
if __name__ == '__main__':
    generate_final_json('1bc8c3e6-8ac3-4de5-8e83-068a82cd640e')
