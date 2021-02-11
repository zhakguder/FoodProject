#!/usr/bin/env python3

import numpy as np
import cv2


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


def is_image_empty(path):
    return cv2.imread(path)


def read_image(path):
    return cv2.imread(path)


def split_image(image, v_n, h_n):
    image_splitter = ImageSplitter(v_n, h_n)
    return image_splitter.split_image_grid(image)


def get_individual_image(splitted_image, v_index, h_index):
    v_n = len(splitted_image)
    h_n = len(splitted_image[0])
    image_splitter = ImageSplitter(v_n, h_n)
    return image_splitter.get_image_at_index(splitted_image, v_index, h_index)


# TODO: add a class to send individual pictures one by one then to convert the predictions to class Candidates
