import os
import torch
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

model_name = "openai/clip-vit-base-patch16"
processor = CLIPProcessor.from_pretrained(model_name)
model = CLIPModel.from_pretrained(model_name)

def preprocess_image(image_path):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt")
    return inputs

def compute_clip_embedding(model, inputs):
    with torch.no_grad():
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

# Directory path containing images
image_dir = ""

# Output file path for the embeddings
output_file = ""

image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

all_embeddings = []

for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    inputs = preprocess_image(image_path)
    embedding = compute_clip_embedding(model, inputs)
    all_embeddings.append(embedding.numpy())

all_embeddings = np.stack(all_embeddings)

np.savez(output_file, embeddings=all_embeddings)

print(f"CLIP embeddings saved to {output_file}")
