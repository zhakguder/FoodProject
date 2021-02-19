#!/usr/bin/env python3


import os

from dotenv import load_dotenv

from food_project.image_classification import \
    compile_test_images_from_recipe_ingredients
from food_project.recipe import connect_to_database

load_dotenv()

uri = os.getenv("MONGODB_URI")
uname = os.getenv("MONGODB_USERNAME")
pwd = os.getenv("MONGODB_PWD")

connect_to_database(uri, uname, pwd)

recipe_ingredients = compile_test_images_from_recipe_ingredients(5)
print(recipe_ingredients)
