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
    return [reverse_map[x] for x in indexes]

def class_probabilities(np_arr):
    probs = tf.nn.softmax(model.predict(np_arr)).numpy()
    pred_probs = {}
    for i in range(len(probs)):
        cls = reverse_map[i]
        cls = parse.unquote_plus(cls)
        pred_probs[cls] = probs[i]
    return pred_probs

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


@app.route("/predict-label/", methods=["POST"])
@limit_content_length(1000 * 1024 * 1024)
def predict():
    image = request.files["image"]
    image = np.array(Image.open(image), dtype=float)
    shp = image.shape
    image = image.reshape(1, *shp) / 255
    # predictions = predict_class_labels(image)
    predictions = class_probabilities(image)
    # result = [parse.unquote_plus(x) for x in predictions]
    print(image)
    print(predictions)
    return Response(predictions, status=200)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="8888")
