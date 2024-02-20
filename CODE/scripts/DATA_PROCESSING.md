# Data Processing 

This documentation file describes the data processing steps that were performed to collect the data used in this project.

## Dataset

The DiffusionDB dataset was used for this project. This dataset is publicly available from HuggingFace at this link: https://huggingface.co/datasets/poloclub/diffusiondb. The dataset contains 2M image-prompt pairs in the original form (over 1.6TB), however, due to storage and hosting cost constraints, we used a subset of 100,000 image-prompts pairs for this project. 

## IAA Scoring

The script to compute image aesthetic assessment scores for all images is located at `scripts/iaa.py`. This script uses the pretrained MUSIQ model to compute IAA scores for all images and saves the scores in the `data/iaa` directory. 

## Image Embeddings

The script to compute image embeddings for all images is located at `scripts/image_embeddings.py`. This script uses the pretrained CLIP model to compute image embeddings for all images and saves the embeddings in the `data/image-emb-2m` directory.

## Neural Network

The notebook to build the neural network described in the paper is located at `CODE/data/other_files/neural_experiment/train_model.ipynb`.

## Analysis

The script to partition the data into the top and bottom 10% of IAA scores is in `scripts/partition.py`. To compare the TF-IDF for the keywords in the good/bad prompts, the `scripts/tf-idf.py` script is used. This script makes use of a JSON object that contains a mapping from every image to its prompt so that prompts can easily be looked up by image ID. The JSON object is created by downloading the prompt metadata with `scripts/prompt-download.py`, converting this CSV to JSON with `scripts/csv-to-json.py`, and reformatting this JSON into an object with `scripts/json-reformat.py`.
