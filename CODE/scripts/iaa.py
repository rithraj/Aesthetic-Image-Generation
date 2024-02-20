import os
import shutil
import json
import _thread
from multiprocessing import Pool
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

PATH_TO_IMAGES = ''
PATH_TO_LOCAL = ''

def main_func(directory, predict_fn):
    try:
        print("Starting with directory: " + directory)
        shutil.copy(f"{PATH_TO_IMAGES}/{directory}", f"{PATH_TO_LOCAL}/{directory}")
        shutil.unpack_archive(f"{PATH_TO_LOCAL}/{directory}", f"{PATH_TO_LOCAL}/{directory[:-4]}")
        os.remove(f"{PATH_TO_LOCAL}/{directory}")
        folder = directory[-4]
        with open(f"predictions-{folder}.txt", 'w') as f:
            for image_path in os.listdir(folder):
                try:
                    image_bytes = tf.io.read_file(os.path.join(folder, image_path))
                    prediction = predict_fn(tf.constant(image_bytes))
                    f.write(f'{image_path},{prediction["output_0"].numpy()}\n')
                except:
                    print("Invalid image: ", image_path)
        shutil.rmtree(f"{PATH_TO_LOCA}/{folder}")
    except Exception as e:
        print("Error: unable to start process")
        print(e)

# with Pool(26) as p:
#     p.map(main_func, directories)

selected_model = 'koniq' #@param ['spaq', 'koniq', 'paq2piq', 'ava']

NAME_TO_HANDLE = {
    # Model trained on SPAQ dataset: https://github.com/h4nwei/SPAQ
    'spaq': 'https://tfhub.dev/google/musiq/spaq/1',

    # Model trained on KonIQ-10K dataset: http://database.mmsp-kn.de/koniq-10k-database.html
    'koniq': 'https://tfhub.dev/google/musiq/koniq-10k/1',

    # Model trained on PaQ2PiQ dataset: https://github.com/baidut/PaQ-2-PiQ
    'paq2piq': 'https://tfhub.dev/google/musiq/paq2piq/1',

    # Model trained on AVA dataset: https://ieeexplore.ieee.org/document/6247954
    'ava': 'https://tfhub.dev/google/musiq/ava/1',
}

model_handle = NAME_TO_HANDLE[selected_model]
model = hub.load(model_handle)
predict_fn = model.signatures['serving_default']

print(f'Loaded model: {selected_model} ({model_handle})')

for i in range(0, 2000):
    num_digits = len(str(i))
    part = ('000000' + str(i))[num_digits:]
    directory = f"part-{part}.zip"
    main_func(directory, predict_fn)