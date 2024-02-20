import csv
import json

csv_file_path = 'cleaned_metadata.csv'
json_file_path = 'metadata.json'

data = []
count = 0
with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if count % 1000 == 0:
            print("PROGRESS: ", count)
        count += 1
        row = {k: v.replace('\x00', '') if isinstance(v, str) else v for k, v in row.items()}
        try:
            data.append({
                'image_name': row['image_name'],
                'prompt': row['prompt']
            })
        except:
            pass

with open(json_file_path, mode='w') as json_file:
    json.dump(data, json_file, indent=2)

print(f'Conversion from CSV to JSON completed. JSON file saved to {json_file_path}')