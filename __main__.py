#!/usr/bin/env python3

import os
from random import choices
from sys import argv

from dotenv import load_dotenv

from food_project.image_classification import (image_classification_model,
                                               set_image_predictor)
from food_project.recipe import (SimilarityController,
                                 SimilarityControllerVisitor,
                                 connect_to_database,
                                 get_processed_ingredients_from_db,
                                 get_recipe_from_db, get_recipe_ids_from_db,
                                 populate_db_images, populate_db_processed,
                                 populate_db_recipes)
from food_project.recipe.matcher import match_score, uniform_score
from food_project.recipe.models import set_recipe_model
from food_project.recipe.recipe import Recipe
from food_project.recipe.similarity import entropy_update

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

unit_type = argv[1]  # can be volume or weight
set_recipe_model(unit_type)
sim_ctrl = SimilarityController()
res = get_processed_ingredients_from_db()
entropy_update(res)
sim_ctrl.load_data()
sim_ctrl_vis = SimilarityControllerVisitor(match_score)
sim_ctrl_vis.visit(sim_ctrl)

raw_data_dir = "data/recipes/raw"
processed_data_dir = "data/recipes/processed"

# for directory in os.listdir(raw_data_dir):
#     populate_db_recipes(os.path.join(raw_data_dir, directory))
#     populate_db_images(os.path.join(raw_data_dir, directory))
# populate_db_processed(os.path.join(processed_data_dir, directory))

all_recipe_ids = get_recipe_ids_from_db()
hits = []
random_ids = choices(all_recipe_ids, k=10)
for recipe_id in random_ids:
    hit = []
    recipe = get_recipe_from_db(int(recipe_id))
    recipe_ingredients = recipe.get("processed_ingredients", "")
    print("*" * 10)
    print(recipe_ingredients)
    print("*" * 10)
    for image in recipe["images"]:
        preds = image_classification_model.get_ingredients(image)
        print("-" * 10)
        print(preds)
        print("-" * 10)
        res = sim_ctrl.handle(preds, n_most_similar_recipes)
        recipe_ids = [int(x) for x in res.index.values]
        for i, id_ in enumerate(recipe_ids):
            print(f"Most similar recipe {i}")
            ingrs = get_recipe_from_db(id_).get("processed_ingredients", [])

            recipe = Recipe(id_, *ingrs)

            res = recipe.importance_ranked_ingredients(use_entropy=False)
            print("*" * 20, unit_type.capitalize(), "only importance", "*" * 20)
            print(res)
            res = recipe.importance_ranked_ingredients()
            print("*" * 20, unit_type.capitalize(), "and entropy importance", "*" * 20)
            print(res)
        hit.append(int(recipe_id) in recipe_ids)
    print("=" * 20)


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
