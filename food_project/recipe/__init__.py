#!/usr/bin/env python3
from food_project.recipe.flat_to_db import populate_db_recipes, populate_db_images, populate_db_processed
from food_project.recipe.db_to_local import get_recipe_from_db
from food_project.recipe.models import RecipeDBInitiator, RecipeFilePathSetter,  RawRecipeGroup, raw_recipe_model
from food_project.recipe.similarity import SimilarityController, SimilarityControllerVisitor

def connect_to_database(uri, uname, pwd):
    rdi = RecipeDBInitiator(uri, uname, pwd)
    raw_recipe_model.accept(rdi)
