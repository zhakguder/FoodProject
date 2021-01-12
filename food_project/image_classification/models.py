#!/usr/bin/env python3
import requests
import os


class DishImageClassificationModel:
    def _init__(self):
        self.uri = None

    def get_ingredients(self, img_path):
        with open(img_path, "rb") as img:
            img_name = os.path.basename(img_path)
            files = {"image": (img_name, img, "multipart/form-data", {"Expires": "0"})}
            with requests.Session() as s:
                r = s.post(self.uri, files=files)
        return r.text

    def accept(self, visitor):
        visitor.visit(self)


class ImageClassificationModelInitiator:
    def __init__(self, uri, port, route):
        self.uri = f"{uri}:{port}/{route}"

    def visit(self, element):
        element.uri = self.uri


image_classification_models = {
    "dish": DishImageClassificationModel(),
    "ingredient": IngredientImageClassificationModel(),
}
