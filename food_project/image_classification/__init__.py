#!/usr/bin/env python3

from food_project.image_classification.crf.potentials import _clique_potentials
from food_project.image_classification.crf.preprocess import (
    GridImagePredictionCollector, read_image)
from food_project.image_classification.models import (
    ImageClassificationModelInitiator, image_classification_model)


def set_image_predictor(uri, port, route):
    icmi = ImageClassificationModelInitiator(uri, port, route)
    image_classification_model.accept(icmi)
    image_classification_model.ready = True
    return image_classification_model


def predict_image(
    image,
    prediction_format="INGR_SERVER",
    image_classification_model=image_classification_model,
):
    if not image_classification_model.ready:
        raise Exception("Set the image predictor first!")
    elif prediction_format == "INGR_SERVER":
        gipc = GridImagePredictionCollector(image_classification_model)
        return gipc.predict_grid_image(image)
    elif prediction_format == "INGR":
        return image_classification_model.get_ingredients(image, with_probs=True)

    else:
        return image_classification_model.get_ingredients(image)


def calculate_clique_potentials():
    print("Calculating clique potentials")
    _clique_potentials.get_frequencies()
    print("Clique potentials calculated")
