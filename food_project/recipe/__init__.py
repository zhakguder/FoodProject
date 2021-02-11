#!/usr/bin/env python3
from food_project.recipe.flat_to_db import (
    populate_db_recipes,
    populate_db_images,
    populate_db_processed,
)
from food_project.recipe.db_to_local import (
    get_recipe_from_db,
    get_recipe_ids_from_db,
    get_processed_ingredients_from_db,
)
from food_project.recipe.models import (
    RecipeDBInitiator,
    RecipeFilePathSetter,
    RawRecipeGroup,
    raw_recipe_model,
)
from food_project.recipe.models import get_recipe_cluster_model
from food_project.recipe.similarity.controller import (
    SimilarityController,
    SimilarityControllerVisitor,
)
import os
import pandas as pd


def connect_to_database(uri, uname, pwd):
    rdi = RecipeDBInitiator(uri, uname, pwd)
    raw_recipe_model.accept(rdi)


def save_cluster_df(path):
    if not os.path.exists(path):
        rcm = get_recipe_cluster_model()
        rcm.export_cluster_df(path)
    else:
        print("File already exists!")


def load_cluster_df(path):
    if not os.path.exists(path):
        raise Except("Cluster file doesn't exist!")
    else:
        return pd.read_pickle(path)
