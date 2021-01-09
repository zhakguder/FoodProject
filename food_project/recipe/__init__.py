#!/usr/bin/env python3
from functools import partial
from food_project.recipe.similarity import SimilarityController, SimilarityControllerVisitor
from food_project.recipe.models import RawRecipeModel, RecipeDBInitiator, RecipeFilePathSetter, RawRecipeReader, RawRecipeGroup


rrm = RawRecipeModel()
rrr = RawRecipeReader()

def connect_to_database(uri, uname, pwd):
    rrmv = RecipeDBInitiator(uri, uname, pwd)
    rrm.accept(rrmv)

def _set_recipe_filename(path, obj):
    rfps = RecipeFilePathSetter(path)
    obj.accept(rfps)

set_recipe_reader_fname = partial(_set_recipe_filename, obj=rrr)
set_recipe_group_dirname = _set_recipe_filename

# def read_recipe(fname):
#     set_recipe_reader_fname(fname)
#     return rrr.read()

def recipe_ids():
    return rrr.recipe_ids

def list_recipe_files(recipe_group_obj):
    if not recipe_group_obj.ready():
        recipe_group_obj.read()
    return recipe_group_obj.process()

def recipe_from_json_by_id(recipe_group_obj, recipe_id):
    return recipe_group_obj.recipe_from_json_by_id(recipe_id)
