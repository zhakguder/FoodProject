#!/usr/bin/env python3
#!/usr/bin/env python
import tensorflow as tf
import numpy as np
import pickle
from PIL import Image
from flask import Flask, request, Response

from urllib import parse
from functools import wraps
import json
from food_project.image_classification import predict_image
from food_project.image_classification.crf.crf_model import CRF
from tempfile import NamedTemporaryFile


app = Flask(__name__)

class Classifier:
    def __init__(self):
        prefix = "/FoodProject/data/image_classification/model/"
        self.model = tf.keras.models.load_model(prefix + "hyvee.best.hdf5")
        with open(prefix + "hyvee_label.dict", "rb") as f:
            mapping = pickle.load(f)
        self.reverse_map = {v: k for k, v in mapping.items()}
        self.ready = True
    def get_ingredients(self, np_arr, with_probs):
        shp = np_arr.shape
        image = np_arr.reshape(1, *shp) / 255
        probs = tf.nn.softmax(self.model.predict(image)).numpy().reshape(-1)
        pred_probs = {}
        for i in range(probs.shape[0]):
            cls = self.reverse_map[i]
            cls = parse.unquote_plus(cls)
            pred_probs[cls] = str(probs[i])
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

    predictions = predict_image(image, image_classification_model=Classifier())

    crf = CRF(9, 5)
    for i in range(3):
        for j in range(3):
            crf.add_node(predictions[i][j])
    prbs, bst = crf.get_best_config(threshold=0.9)
    resp = json.loads({'prbs': prbs, 'best': bst})
    return Response(resp, status=200)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="8888")
