import os
import matplotlib.pyplot as plt

def read_scores(file_path):
    scores = []
    with open(file_path, 'r') as file:
        for line in file:
            _, score = line.strip().split(',')
            scores.append(float(score))
    return scores

directory_path = '../data/iaa'

all_scores = []

for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory_path, filename)
        scores = read_scores(file_path)
        all_scores.extend(scores)

plt.hist(all_scores, bins=20, color='blue', alpha=0.7)
plt.title('Distribution of IAA Scores - All Files')
plt.xlabel('IAA Scores')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
