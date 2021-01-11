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
model = tf.keras.models.load_model('/FoodProject/data/image_classification/model/hyvee.best.hdf5')
logits = model.predict(images_for_prediction)

# partition = 'validation'
# path = partition + '_ds'
# spec = (tf.TensorSpec(shape=(None, 256, 256, 3), dtype=tf.float32, name=None), tf.TensorSpec(shape=(None,), dtype=tf.int32, name=None))

# val_data = tf.data.experimental.load(path, spec)


# val_data_x = val_data.map(lambda x, y: x)
# val_data_y = val_data.map(lambda x, y: y)
# preds = trained_model.predict(val_data_x)

predicted_class_indexes = tf.argmax(tf.nn.softmax(logits), axis=1)

with open('hyvee_label.dict', 'rb') as f:
    mapping = pickle.load(f)

reverse_map = {v:k for k,v in mapping.items()}
predicted_classes = [reverse_map[x] for x in predicted_class_indexes]
print(predicted_classes)
