import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Read content from predictions.txt to identify filenames and scores
with open('output_partitioned_bottom_10.txt', 'r') as predictions_file:
    filenames = [line.strip().split(',')[0] for line in predictions_file]

# Read content from the JSON file
with open('metadata-object.json', 'r') as json_file:
    data = json.load(json_file)

# Extract the relevant data
documents = [data[filename] for filename in filenames]

# Create the TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the documents
tfidf_matrix = vectorizer.fit_transform(documents)

# Get the feature names (terms)
feature_names = vectorizer.get_feature_names()

# Calculate the average TF-IDF values for each term
average_tfidf_per_term = np.mean(tfidf_matrix, axis=0)

# Sort terms based on average TF-IDF values
sorted_term_indices = np.argsort(average_tfidf_per_term).flatten()

# Convert to list
sorted_term_indices = sorted_term_indices.tolist()[0]

# Print the top terms and their average TF-IDF values
num_top_terms = 20
top_terms = [feature_names[i] for i in sorted_term_indices[-num_top_terms:]]
top_tfidf_values = [average_tfidf_per_term[0, i] for i in sorted_term_indices[-num_top_terms:]]

for term, tfidf_value in zip(top_terms, top_tfidf_values):
    print(f"{term}: {tfidf_value}")

# Save to file
with open('bottom_10_tfidf.txt', 'w') as txtfile:
    for term, tfidf_value in zip(top_terms, top_tfidf_values):
        txtfile.write(f"{term}: {tfidf_value}\n")
