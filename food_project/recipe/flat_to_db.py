#!/usr/bin/env python3
import os
from functools import partial
from food_project.recipe.models import RecipeFilePathSetter,  raw_recipe_model, raw_recipe_reader, RawRecipeGroup, RawRecipeImageGroup, RawImageGroup, ProcessedRecipeGroup, ProcessedRecipeReader

def set_recipe_filename(path, obj):
    rfps = RecipeFilePathSetter(path)
    obj.accept(rfps)

set_recipe_reader_fname = partial(set_recipe_filename, obj=raw_recipe_reader)
set_group_dirname = set_recipe_filename

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



def save_recipe_image_paths(recipe_image_folder):
    # recipe_id = os.path.basename(recipe_id)
    rig = RawImageGroup()
    set_group_dirname(recipe_image_folder, rig)
    recipe_id = os.path.basename(recipe_image_folder)
    images = list_group_files(rig)
    raw_recipe_model.update(recipe_id, {'images': images})

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
    for recipe_group in list_group_files(rcig):
        save_recipe_image_paths(recipe_group)

def populate_db_processed(path):
    prg = ProcessedRecipeGroup()
    set_group_dirname(path, prg)
    for recipe in list_group_files(prg):
        prr = ProcessedRecipeReader()
        set_recipe_filename(recipe, prr)
        if not prr.ready():
            data = prr.read()
        print(data)
