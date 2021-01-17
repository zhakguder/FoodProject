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
    get_recipe_ids_from_db,
    populate_db_processed,
)
from food_project.image_classification import (
    set_image_predictor,
    image_classification_model,
)
from random import choices
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
#     populate_db_recipes(os.path.join(raw_data_dir, directory))
#     populate_db_images(os.path.join(raw_data_dir, directory))
    populate_db_processed(os.path.join(processed_data_dir, directory))

# all_recipe_ids = get_recipe_ids_from_db()
# hits = []
# random_ids = choices(all_recipe_ids, k=10)
# for recipe_id in random_ids:
#     hit = []
#     breakpoint()
#     recipe = get_recipe_from_db(int(recipe_id))
#     recipe_ingredients = recipe.get('processed_ingredients', '')
#     print("*"*10)
#     print(recipe_ingredients)
#     print("*"*10)
#     for image in recipe["images"]:
#         preds = image_classification_model.get_ingredients(image)
#         print('-'*10)
#         print(preds)
#         print('-'*10)
#         res = sim_ctrl.handle(preds, n_most_similar_recipes)
#         recipe_ids = [int(x) for x in res.index.values]
#         for id_ in recipe_ids:
#             print(get_recipe_from_db(id_).get('processed_ingredients', []))
#         hit.append(int(recipe_id) in recipe_ids)
#     print('='*20)


#     hits.append(hit)
# print(hits)
# recipe = get_recipe_from_db(277888)
# print(recipe['name'])
# print(recipe['processed_ingredients'])
# print("PREDICTIONS")
# for image in recipe['images']:
#     preds = image_classification_model.get_ingredients(image)
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
