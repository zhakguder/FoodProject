#!/usr/bin/env python3

from food_project.image_classification.models import (
    image_classification_model,
    ImageClassificationModelInitiator,
)


def set_image_predictor(uri, port, route):
    icmi = ImageClassificationModelInitiator(uri, port, route)
    image_classification_model.accept(icmi)
    return image_classification_model
