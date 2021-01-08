#!/usr/bin/env python3
from food_project.recipe.similarity import SimilarityController, SimilarityControllerVisitor
from food_project.recipe.models import RawRecipeModel, RecipeDBInitiator, RecipeFilePathSetter

rrm = RawRecipeModel()

def connect_to_database(uri, uname, pwd):
    rrmv = RecipeDBInitiator(uri, uname, pwd)
    rrm.accept(rrmv)
    return rrm

def set_recipe_file_pathprefix(prefix):
    rfps = RecipeFilePathSetter(prefix)
    rrm.accept(rfps)
    return rrm
