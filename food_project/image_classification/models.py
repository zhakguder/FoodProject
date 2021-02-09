#!/usr/bin/env python3
import requests
import os


class ImageClassificationModel:
    def _init__(self):
        self.uri = None
        self._ready = False

    @property
    def ready(self):
        return self._ready

    @ready.setter
    def ready(self, ready_or_not):
        self._ready = ready_or_not

    def get_ingredients(self, img_path, with_probs=False):
        with open(img_path, "rb") as img:
            img_name = os.path.basename(img_path)
            files = {"image": (img_name, img, "multipart/form-data", {"Expires": "0"})}
            with requests.Session() as s:
                r = s.post(self.uri, files=files)
            if with_probs:
                return r
        return [x.strip() for x in r.text.split(",")]

    def accept(self, visitor):
        visitor.visit(self)


class ImageClassificationModelInitiator:
    def __init__(self, uri, port, route):
        self.uri = f"{uri}:{port}/{route}"

    def visit(self, element):
        element.uri = self.uri


image_classification_model = ImageClassificationModel()
