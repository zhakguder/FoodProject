#!/usr/bin/env python3
import os

import cv2
import numpy as np


class TestImageCompiler:
    def __init__(self, n):
        """Args:
        n: number of grids in nxn placements of image
        """
        self.n = n
        self.single_image_width = 28
        self.single_image_height = 28
        self.single_image_size = lambda: (
            self.single_image_width,
            self.single_image_height,
        )
        self.n_color = 3  # for RGB
        self.img_empty_grid = lambda height, width: np.zeros(
            (height * self.n, width * self.n, self.n_color), np.uint8
        )

    def compile_test_image(self, *image_paths):
        width, height = self.single_image_size()
        canvas = self.img_empty_grid(height, width).copy()

        n_images = len(image_paths)

        for i in range(self.n):
            for j in range(self.n):
                image_idx = i * self.n + j

                if image_idx < n_images:
                    image_path = image_paths[image_idx]
                    image = GridImage(image_path, *self.single_image_size())
                    y = i * height
                    x = j * width
                    canvas[y : y + height, x : x + width, :] = image.image
        return canvas

    @staticmethod
    def write(path, canvas):
        cv2.imwrite(path, canvas)

    def accept(self, visitor):
        visitor.visit(self)


class GridImage:
    def __init__(self, path, width=28, height=28):
        self.path = path
        self._image = cv2.imread(path)
        self.size = (width, height)
        self._image = cv2.resize(self.image, self.size)

    @property
    def image(self):
        if self._image is None:
            raise Exception("Image not read yet")
        return self._image

    def resize(self, size):
        if self.size == size:
            return self
        return GridImage(self.path, size)


class ImageSizeSetter:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def visit(self, element):
        element.single_image_width = self.width
        element.single_image_height = self.height


def read_individual_image(path):
    gi = GridImage(path, 200, 200)
    return gi.image


def make_test_image(
    test_image_dir: str,
    n: int,
    image_ext: str = ".jpeg",
    write: bool = False,
    size: int = 200,
    **kwargs
) -> np.array:
    """Creates a nxn image grid consisting of images in the folder. If folder
        contains more than nxn images randomly places nxn of the images in the
        grid.

        Individual images are resized to sizexsize before placing in the grid.

    Args:

        n: number of grids in nxn placements of images.

        k: number of images to use

        test_image_dir: relative folder from which to get test images from

        Kwargs:
            path: path to write the compiled image if write is True

    Returns:

        canvas: an nxn image grid

    """

    path = kwargs["path"] if "path" in kwargs else None

    tic = TestImageCompiler(n)
    _set_canvas_grid_size(tic, size)

    get_absolute = lambda x: os.path.join(test_image_dir, x)
    image_paths = os.listdir(test_image_dir)

    image_paths = [get_absolute(x) for x in image_paths if x.endswith(image_ext)]
    canvas = tic.compile_test_image(*image_paths)
    if write:
        tic.write(path, canvas)
    return canvas


def _set_canvas_grid_size(comp: TestImageCompiler, size: int) -> None:
    iss = ImageSizeSetter(size, size)
    iss.visit(comp)
