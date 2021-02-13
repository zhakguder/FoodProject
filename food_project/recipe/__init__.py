#!/usr/bin/env python3
import os

import pandas as pd

from food_project.recipe.db_to_local import (get_processed_ingredients_from_db,
                                             get_recipe_from_db,
                                             get_recipe_ids_from_db)
from food_project.recipe.flat_to_db import (populate_db_images,
                                            populate_db_processed,
                                            populate_db_recipes)
from food_project.recipe.models import (RawRecipeGroup, RecipeDBInitiator,
                                        RecipeFilePathSetter,
                                        get_recipe_cluster_model,
                                        raw_recipe_model)
from food_project.recipe.similarity.controller import (
    SimilarityController, SimilarityControllerVisitor)


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
