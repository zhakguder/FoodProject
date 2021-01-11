#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from food_project.recipe import SimilarityController, SimilarityControllerVisitor
from food_project.recipe.matcher import match_score, uniform_score
from food_project.recipe import connect_to_database, populate_db_recipes, populate_db_images, get_recipe_from_db
from food_project.image_prediction import set_image_predictor, image_classification_model

load_dotenv()
uri = os.getenv("MONGODB_URI")
uname = os.getenv("MONGODB_USERNAME")
pwd = os.getenv("MONGODB_PWD")

classification_uri = os.getenv("CLASSIFICATION_URI")
classification_port = os.getenv("CLASSIFICATION_PORT")
classification_route = os.getenv("CLASSIFICATION_ROUTE")


connect_to_database(uri, uname, pwd)
set_image_predictor(classification_uri, classification_port, classification_route)


sim_ctrl = SimilarityController()
sim_ctrl_vis = SimilarityControllerVisitor(match_score)
sim_ctrl_vis.visit(sim_ctrl)

# populate_db_recipes('data/raw/ArgentinianRecipes')
# populate_db_images('data/raw/ArgentinianRecipes')
recipe = get_recipe_from_db(277888)
print(recipe['name'])
for image in recipes['images']:
    preds = image_classification_model.get_ingredients(image)
    preds = [x.strip() for x in preds.split(',')]
    res = sim_ctrl.handle(preds, 100)
    recipe_ids = [int(x) for x in res.index.values]
    for recipe_id in recipe_ids:
        try:
            recipe = get_recipe_from_db(recipe_id)
            print(recipe['name'])
            print(recipe['ingredients'])
        except:
            pass


# print(recipe_ids())

# test = ["apple", "cinnamon", "walnut"]

# mask = sim_ctrl.handle(test, 5)


# Documentation for mongodb docker: https://hub.docker.com/_/mongo
