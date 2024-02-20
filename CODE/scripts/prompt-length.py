import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt

# Read content from predictions.txt to identify filenames and scores
with open('output_partitioned_top_10.txt', 'r') as predictions_file:
    filenames = [line.strip().split(',')[0] for line in predictions_file]

# Read content from the JSON file
with open('./lfs/metadata-object.json', 'r') as json_file:
    data = json.load(json_file)

# Extract the relevant data
good_documents = [data[filename] for filename in filenames]

good_average_length = np.mean([len(document) for document in good_documents])

with open('output_partitioned_bottom_10.txt', 'r') as predictions_file:
    filenames = [line.strip().split(',')[0] for line in predictions_file]

# Read content from the JSON file
with open('./lfs/metadata-object.json', 'r') as json_file:
    data = json.load(json_file)

bad_documents = [data[filename] for filename in filenames]

bad_average_length = np.mean([len(document) for document in bad_documents])

print(f"Average length of good prompts: {good_average_length}")
print(f"Average length of bad prompts: {bad_average_length}")

# Plot the distribution of lengths
plt.hist([len(document) for document in good_documents], bins=20, alpha=0.5, label='Good')
plt.hist([len(document) for document in bad_documents], bins=20, alpha=0.5, label='Bad')
plt.legend(loc='upper right')
plt.xlabel('Length')
plt.ylabel('Frequency')
plt.title('Distribution of Prompt Lengths')
plt.show()

# Save to file
with open('top_10_length.txt', 'w') as txtfile:
    txtfile.write(f"Average length: {good_average_length}\n")
with open('bottom_10_length.txt', 'w') as txtfile:
    txtfile.write(f"Average length: {bad_average_length}\n")