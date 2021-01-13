#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from food_project.recipe import SimilarityController, SimilarityControllerVisitor
from food_project.recipe.matcher import match_score, uniform_score
from food_project.recipe import (
    connect_to_database,
    populate_db_recipes,
    populate_db_images,
    get_recipe_from_db,
    populate_db_processed,
)
from food_project.image_classification import (
    set_image_predictor,
    image_classification_model,
)

load_dotenv()


classification_type = "DISH"  # or INGR

uri = os.getenv("MONGODB_URI")
uname = os.getenv("MONGODB_USERNAME")
pwd = os.getenv("MONGODB_PWD")
classification_uri = os.getenv("SERVER_URI")

prefix = classification_type + "_CLASS_"
classification_port = os.getenv(prefix + "PORT")
classification_route = os.getenv(prefix + "ROUTE")

n_most_similar_recipes = int(os.getenv("N_SIMILAR"))

connect_to_database(uri, uname, pwd)
set_image_predictor(classification_uri, classification_port, classification_route)


sim_ctrl = SimilarityController()
sim_ctrl_vis = SimilarityControllerVisitor(match_score)
sim_ctrl_vis.visit(sim_ctrl)

raw_data_dir = "data/recipes/raw"
processed_data_dir = "data/recipes/processed"

for directory in os.listdir(raw_data_dir):
    populate_db_recipes(os.path.join(raw_data_dir, directory))
    populate_db_images(os.path.join(raw_data_dir, directory))
    populate_db_processed(os.path.join(processed_data_dir, directory))

# recipe = get_recipe_from_db(277888)
# print(recipe['name'])
# print(recipe['processed_ingredients'])
# print("PREDICTIONS")
# for image in recipe['images']:
#     preds = dish_image_classification_model.get_ingredients(image)
#     preds = [x.strip() for x in preds.split(',')]
#     res = sim_ctrl.handle(preds, n_most_similar_recipes)
#     recipe_ids = [int(x) for x in res.index.values]
#     for recipe_id in recipe_ids:
#         try:
#             recipe = get_recipe_from_db(recipe_id)
#             print(recipe['name'])
#             print(recipe['processed_ingredients'])
#         except:
#             pass

# To copy processed recipes from HCC to pandas
# find  ArgentinianRecipes -type f -regextype sed -regex ".*[0-9]\.out" -exec scp '{}' zeynep@sbbi-panda.unl.edu:/home/zeynep/projects/FoodProject/backend/data/processed/ArgentinianRecipes ';'
#
# To mv jsons in original_recipe_data folders nested e.g. in American recipes
# find .. -name \*data.json -exec sh -c 'new=$(echo "{}" | tr "/" "-" | tr " " "_"| sed s/..// |sed s/original_recipes_info//|sed s/-//g); mv "{}" "$new"' \;
# find .. -type d -regextype sed -regex ".*imgs/.*[0-9]*" -exec  mv '{}' . ';'
# mkdir original_recipes_info imgs
