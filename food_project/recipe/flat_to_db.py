#!/usr/bin/env python3
from functools import partial
from food_project.recipe.models import RecipeFilePathSetter,  raw_recipe_model, raw_recipe_reader, RawRecipeGroup, RawRecipeImageGroup

def _set_recipe_filename(path, obj):
    rfps = RecipeFilePathSetter(path)
    obj.accept(rfps)

set_recipe_reader_fname = partial(_set_recipe_filename, obj=raw_recipe_reader)
set_group_dirname = _set_recipe_filename

def recipe_ids():
    if not raw_recipe_reader.ready:
        raw_recipe_reader.read()
    return raw_recipe_reader.recipe_ids

def list_group_files(group_obj):
    return group_obj.process()

def save_recipe_by_id(recipe_id):
    try:
        data = raw_recipe_reader.recipe_by_id(recipe_id)
    except Exception as e:
        raise e
    raw_recipe_model.save(data)

def populate_db_recipes(path):
    rcg = RawRecipeGroup()
    set_group_dirname(path, rcg)
    for recipe_file in list_group_files(rcg):
        set_recipe_reader_fname(recipe_file)
        ids = recipe_ids()
        for id_ in ids:
            save_recipe_by_id(id_)

def populate_db_images(path):
    rcig = RawRecipeImageGroup()
    set_group_dirname(path, rcig)
