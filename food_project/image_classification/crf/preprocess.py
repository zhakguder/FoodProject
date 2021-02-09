#!/usr/bin/env python3
import os
import numpy as np
import cv2
from PIL import Image
from tempfile import NamedTemporaryFile
import json
from food_project.image_classification.crf.prediction_class_clusters import (
    ClassCandidates,
)


class ImageSplitter:
    def __init__(self, n, m):

        """Args:

                n: number of desired images along height
                m: number of desired images along width
        """

        self.n = n
        self.m = m

    def split_image_grid(self, image):
        vertical_splitted = np.split(image, self.n, axis=0)
        horizontal_splitted = [np.split(x, self.m, axis=1) for x in vertical_splitted]
        return horizontal_splitted

    def get_image_at_index(self, image, v_index, h_index):
        return image[v_index][h_index]

    def set_grid_no(self, v_n, h_n):
        self.n = v_n
        self.m = h_n


def is_image_empty(image):
    return len(np.unique(image)) == 1


def read_image(path):
    return cv2.imread(path)


def arr_to_jpeg(arr, path):
    im = Image.fromarray(arr)
    im.save(path)


def split_image(image, v_n, h_n):
    image_splitter = ImageSplitter(v_n, h_n)
    return image_splitter.split_image_grid(image)


def get_individual_image(splitted_image, v_index, h_index):
    v_n = len(splitted_image)
    h_n = len(splitted_image[0])
    image_splitter = ImageSplitter(v_n, h_n)
    return image_splitter.get_image_at_index(splitted_image, v_index, h_index)


class GridImageCollector:
    def __init__(self, grid_image, v_n, h_n):
        self.grid_image = grid_image
        self._v_n = v_n
        self._h_n = h_n

    @property
    def splitted(self):
        return split_image(self.grid_image, self.n_vertical, self.n_horizontal)

    def __getitem__(self, idx):
        return get_individual_image(self.splitted, idx[0], idx[1])

    @property
    def n_vertical(self):
        return self._v_n

    @property
    def n_horizontal(self):
        return self._h_n


class GridImagePredictionCollector:
    def __init__(self, classifier_client):
        self.classifier_client = classifier_client
        self.predictions = None
        self.ready = False

    def __getitem__(self, idx):
        if not self.ready:
            raise Exception("Individual image predictions not performed yet!")
        return self.predictions[idx[0]][idx[1]]

    def __setitem__(self, idx, value):
        self.predictions[idx[0]][idx[1]] = value

    def predict_grid_image(self, grid_image):
        preds = []
        # TODO: don't hardcode 3x3
        grid_image = GridImageCollector(grid_image, 3, 3)
        for i in range(grid_image.n_vertical):
            preds_row = []
            for j in range(grid_image.n_horizontal):
                image = grid_image[i, j]
                if not is_image_empty(image):
                    temp = NamedTemporaryFile(suffix=".jpeg")

                    arr_to_jpeg(grid_image[i, j], temp.name)
                    pred = self.classifier_client.get_ingredients(
                        temp.name, with_probs=True
                    )
                    temp.close()
                else:
                    pred = {"empty": 1}
                preds_row.append(ClassCandidates(pred))
            preds.append(preds_row)
        self.predictions = preds
        self.ready = True
        return self.predictions


# TODO: Pictures are shifted in the grid!!!
