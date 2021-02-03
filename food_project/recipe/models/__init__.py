#!/usr/bin/env python3

from food_project.recipe.models.recipe_models import (
    RecipeModelVolumeFactory,
    RecipeModelWeightFactory,
)

model_type = None
model_factory = None
recipe_ingredient_model = None
recipe_cluster_model = None


def set_recipe_model(modeltype="volume"):
    global model_type
    model_type = model_type
    _set_recipe_model_factory()
    _set_recipe_ingredient_model()
    _set_recipe_cluster_model()


def _set_recipe_model_factory():
    global model_factory
    if model_type == "volume":
        model_factory = RecipeModelVolumeFactory()
    elif model_type == "weight":
        model_factory = RecipeModelWeightFactory()


def _set_recipe_ingredient_model():
    global recipe_ingredient_model
    recipe_ingredient_model = model_factory.create_ingredient_model()


def _set_recipe_cluster_model():
    global recipe_cluster_model
    recipe_cluster_model = model_factory.create_cluster_model()


def get_recipe_ingredient_model():
    return recipe_ingredient_model


def get_recipe_cluster_model():
    return recipe_cluster_model
