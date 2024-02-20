from urllib.request import urlretrieve
import pandas as pd

# Download the parquet table
table_url = f'https://huggingface.co/datasets/poloclub/diffusiondb/resolve/main/metadata.parquet'
urlretrieve(table_url, 'metadata.parquet')

# Read the table using Pandas
metadata_df = pd.read_parquet('metadata.parquet')
metadata_df.head()
predictions = pd.read_csv('predictions-part-000001.txt', names=['image_name', 'iaa_score'])
predictions
import json

metadata_df = metadata_df.drop(columns=['timestamp'])
result_dict = {}
for i in range(1, 101):
    predictions = pd.read_csv(f'../../data/iaa/predictions-part-{str(i).zfill(6)}.txt', names=['image_name', 'iaa_score'])
    merged = metadata_df.merge(predictions, on='image_name', how='inner')
    for index, row in merged.iterrows():
        key = row['image_name']
        other_data = row.drop('image_name').to_dict()
        if str(i) not in result_dict:
            result_dict[str(i)] = {key: other_data}
        else:
            result_dict[str(i)][key] = other_data

result_dict
with open('master-predict.json', 'w') as json_file:
    json.dump(result_dict, json_file, indent=4)
search_vals = {}
for key, value in result_dict.items():
    for k, v in value.items():
        v['id'] = k
        search_vals.update({k: v})

with open('master-search.json', 'w') as json_file:
    json.dump(search_vals, json_file, indent=4)
vals = []
for key, value in result_dict.items():
    for k, v in value.items():
        v['id'] = k
        vals.append(v)

df = pd.DataFrame(vals)
df.head()
df['iaa_score'].describe()