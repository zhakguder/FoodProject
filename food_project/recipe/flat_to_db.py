#!/usr/bin/env python3
from functools import partial
from food_project.recipe.models import RecipeFilePathSetter,  raw_recipe_model, raw_recipe_reader, RawRecipeGroup


def _set_recipe_filename(path, obj):
    rfps = RecipeFilePathSetter(path)
    obj.accept(rfps)

set_recipe_reader_fname = partial(_set_recipe_filename, obj=raw_recipe_reader)
set_recipe_group_dirname = _set_recipe_filename

def recipe_ids():
    if not raw_recipe_reader.ready:
        raw_recipe_reader.read()
    return raw_recipe_reader.recipe_ids

def list_recipe_files(recipe_group_obj):
    return recipe_group_obj.process()

def save_recipe_by_id(recipe_id):
    raw_recipe_model.save(recipe_id, raw_recipe_reader)

def populate_db(path):
    rcg = RawRecipeGroup()
    set_recipe_group_dirname('data/raw/ArgentinianRecipes', rcg)
    for recipe_file in list_recipe_files(rcg):
        set_recipe_reader_fname(recipe_file)
        ids = recipe_ids()
        for id_ in ids:
            save_recipe_by_id(id_)
