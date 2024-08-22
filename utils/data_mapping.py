import json

def map_data_to_objects(objects, descriptions, texts, summaries):
    mapping = {}
    for obj_id, (desc, text, summary) in enumerate(zip(descriptions, texts, summaries)):
        mapping[obj_id] = {
            "description": desc,
            "extracted_text": text,
            "summary": summary
        }
    return mapping

def save_mapping_to_json(mapping, output_path):
    with open(output_path, 'w') as f:
        json.dump(mapping, f)
