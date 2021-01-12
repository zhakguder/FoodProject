#!/usr/bin/env python
import tensorflow as tf
import numpy as np
import pandas as pd
import pickle
from sys import argv
from PIL import Image
from flask import Flask, request, Response
from urllib import parse
from functools import wraps
app = Flask(__name__)


# image_paths = argv[1:]

# f = Image.open

# images_for_prediction = np.stack([f(x) for x in image_paths])
prefix = "/FoodProject/data/image_classification/model/"

model = tf.keras.models.load_model(prefix + "hyvee.best.hdf5")
with open(prefix + "hyvee_label.dict", "rb") as f:
    mapping = pickle.load(f)

reverse_map = {v: k for k, v in mapping.items()}


def predict_class_indexes(np_arr):
    logits = model.predict(np_arr)
    return tf.argmax(tf.nn.softmax(logits), axis=1)

def predict_class_labels(arr):
    indexes = predict_class_indexes(arr).numpy()
    return [reverse_map[x].replace('_', ' ') for x in indexes]

def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/predict-label/', methods=['POST'])
@limit_content_length(1000 * 1024 * 1024)
def predict():
    image = request.files['image']
    shp = image.shape
    image = image.reshape(1, *shp)
    prediction = predict_class_labels(image)
    result = parse.unquote_plus(prediction)
    return Response(result, status=200)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port='8888')
