#!/usr/bin/env python3

from food_project.image_classification.models import image_classification_model, ImageClassificationModelInitiator
from food_project.image_classification.crf.preprocess import GridImagePredictionCollector, read_image

def set_image_predictor(uri, port, route):
    icmi = ImageClassificationModelInitiator(uri, port, route)
    image_classification_model.accept(icmi)
    image_classification_model.ready = True
    return image_classification_model

def predict_image(image, prediction_format):
    if not image_classification_model.ready:
        raise Exception("Set the image predictor first!")
    if prediction_format == 'DISH':
        return image_classification_model.get_ingredients(image)
    elif prediction_format == 'INGR':
        gipc = GridImagePredictionCollector(image_classification_model)
        return gipc.predict_grid_image(image)
