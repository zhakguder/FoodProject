#!/usr/bin/env python3
import json
import os
import random

import cv2
import numpy as np

from food_project.image_classification.crf.prediction_class_clusters import (
    _get_prediction_class_list,
)
from food_project.recipe import (
    get_processed_ingredients_from_db,
    get_recipe_from_db,
    get_recipe_ids_from_db,
)
from food_project.util import matchsubstring

ingredient_data_path = "data/image_classification/hyvee"


class IngredientImagePaths:
    def __init__(self):
        random.seed(42)

    def get_image_path_for_class(self, cls):
        image_folder = os.path.join(ingredient_data_path, cls)
        paths = os.listdir(image_folder)
        chosen = random.choice(paths)
        return os.path.join(image_folder, chosen)


ingredient_image_paths = IngredientImagePaths()


def get_random_ingredient_path_from_class(cls):
    return ingredient_image_paths.get_image_path_for_class(cls)


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


class GridImageLabels:
    def __init__(self, save_path):
        self.save_path = save_path

    def save_id(self, id_, labels):
        tmp = {}
        if os.path.exists(self.save_path):
            with open(self.save_path, 'r') as f:
                tmp = json.load(f)

        with open(self.save_path, "w") as f:
            tmp.update({id_: labels})
            json.dump(tmp, f)

class RecipeIngredientLister:
    # def __init__(self, recipe_db):
    # self.recipe_db = recipe_db
    def __init__(self, label_file_path):
        self.recipe_ids = get_recipe_ids_from_db()
        self.recipes = {}
        self.recipe_ingredients = {}
        self.seed = 42
        random.seed(self.seed)
        self.valid_classes = _get_prediction_class_list()
        self.label_writer = GridImageLabels(label_file_path)

    def _random_recipes(self, k):
        if not self.recipes:
            self.random_recipe_ids = random.choices(self.recipe_ids, k=k)
            self.recipes = {
                id_: get_recipe_from_db(int(id_)) for id_ in self.random_recipe_ids
            }

        return self.recipes

    def _ingredient_matching_class(self, ingredient):
        ingredient = ingredient.lower()
        max_score = 0
        best_match = ""
        for cls in self.valid_classes:
            score = matchsubstring(cls, ingredient)
            if score > max_score:
                best_match = cls
                max_score = score
        return best_match

    def _get_recipe_ingredients(self, recipe_id):
        return [
            self._ingredient_matching_class(x)
            for x in self.recipes[recipe_id].get("processed_ingredients", [])
        ]

    def get_recipe_ingredient_images(self, n_recipes, size):
        recipes = self._random_recipes(n_recipes)
        if not self.recipe_ingredients:
            for recipe_id, _ in recipes.items():
                self.recipe_ingredients[recipe_id] = list(
                    set(self._get_recipe_ingredients(recipe_id))
                )

                image_paths = [
                    get_random_ingredient_path_from_class(x)
                    for x in self.recipe_ingredients[recipe_id]
                ]
                tic = TestImageCompiler(3)
                iss = ImageSizeSetter(size, size)
                iss.visit(tic)
                try:
                    image = tic.compile_test_image(*image_paths)
                    path = os.path.join(
                        "data/image_classification", "grid", f"{recipe_id}.jpeg"
                    )
                    tic.write(path, image)
                    self.label_writer(self.recipe_ingredients[recipe_id])
                except:
                    pass



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
    **kwargs,
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
