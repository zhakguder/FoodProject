#!/usr/bin/env python3
from functools import partial
from food_project.recipe.similarity import SimilarityController, SimilarityControllerVisitor
from food_project.recipe.models import RawRecipeModel, RecipeDBInitiator, RecipeFilePathSetter, RawRecipeReader, RawRecipeGroup


rrm = RawRecipeModel()
rrr = RawRecipeReader()

def connect_to_database(uri, uname, pwd):
    rrmv = RecipeDBInitiator(uri, uname, pwd)
    rrm.accept(rrmv)

def _set_recipe_filename(prefix, obj):
    rfps = RecipeFilePathSetter(prefix)
    obj.accept(rfps)

set_recipe_reader_fname = partial(_set_recipe_filename, obj=rrr)
set_recipe_group_dirname = _set_recipe_filename

def read_recipe(fname):
    set_recipe_reader_fname(fname)
    return rrr.read()

def recipe_ids():
    return rrr.recipe_ids

def list_recipes(obj):
    return obj.process()
