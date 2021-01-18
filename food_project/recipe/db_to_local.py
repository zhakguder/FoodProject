#!/usr/bin/env python3

from food_project.recipe.models import raw_recipe_model

def get_recipe_from_db(id_):
    return raw_recipe_model.load(id_)

def get_recipe_ids_from_db():
    return raw_recipe_model.retrieve_field('recipe_ID')
def get_processed_ingredients_from_db():
    return raw_recipe_model.retrieve_field('processed_ingredients')
