import json

def save_metadata(metadata, file_path):
    """Save metadata to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def load_metadata(file_path):
    """Load metadata from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def map_data_to_objects(objects, metadata):
    """Map data to each object and return a mapping dictionary."""
    mapping = {}
    for obj_id, obj_data in objects.items():
        mapping[obj_id] = {
            'description': metadata.get(obj_id, {}).get('description', ''),
            'text_data': metadata.get(obj_id, {}).get('text_data', ''),
            'attributes': metadata.get(obj_id, {}).get('attributes', {}),
        }
    return mapping
