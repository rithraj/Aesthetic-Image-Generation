import json

json_file_path = 'metadata.json'
output_file_path = 'metadata-object.json'

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

image_prompt_mapping = {item['image_name']: item['prompt'] for item in data}

with open(output_file_path, 'w') as output_file:
    json.dump(image_prompt_mapping, output_file, indent=2)

print(f'Conversion completed. JSON file saved to {output_file_path}')
