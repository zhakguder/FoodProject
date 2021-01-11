#!/usr/bin/env python
import tensorflow as tf
import numpy as np
import pandas as pd
import pickle
from sys import argv
from PIL import Image

image_paths = argv[1:]
f = Image.open
images_for_prediction = np.stack([f(x) for x in image_paths])
prefix = '/FoodProject/data/image_classification/model/'

model = tf.keras.models.load_model(prefix+'hyvee.best.hdf5')
logits = model.predict(images_for_prediction)


predicted_class_indexes = tf.argmax(tf.nn.softmax(logits), axis=1)

with open(prefix+'hyvee_label.dict', 'rb') as f:
    mapping = pickle.load(f)

reverse_map = {v:k for k,v in mapping.items()}
predicted_classes = [reverse_map[x] for x in predicted_class_indexes.numpy()]
print(predicted_classes)
