#!/usr/bin/env python3
from food_project.recipe.flat_to_db import populate_db
from food_project.recipe.models import RecipeDBInitiator, RecipeFilePathSetter,  RawRecipeGroup, raw_recipe_model
from food_project.recipe.similarity import SimilarityController, SimilarityControllerVisitor

def connect_to_database(uri, uname, pwd):
    rrmv = RecipeDBInitiator(uri, uname, pwd)
    raw_recipe_model.accept(rrmv)
