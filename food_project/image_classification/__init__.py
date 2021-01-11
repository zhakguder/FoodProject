#!/usr/bin/env python3

from food_project.image_prediction.models import image_classification_models, ImageClassificationModelInitiator

def set_image_predictor(uri, port, route, classification_task):
    image_classification_model = image_classification_models[classification_task]
    icmi = ImageClassificationModelInitiator(uri, port, route)
    image_classification_model.accept(icmi)
    return image_classification_model
