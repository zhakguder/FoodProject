#!/usr/bin/env python3

from food_project.recipe.models import raw_recipe_model

def get_recipe_from_db(id_):
    return raw_recipe_model.load(id_)
