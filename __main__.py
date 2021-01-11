#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from food_project.recipe import SimilarityController, SimilarityControllerVisitor
from food_project.recipe.matcher import match_score, uniform_score
from food_project.recipe import connect_to_database, populate_db_recipes, populate_db_images, get_recipe_from_db
from food_project.image_prediction import set_image_predictor

load_dotenv()
uri = os.getenv("MONGODB_URI")
uname = os.getenv("MONGODB_USERNAME")
pwd = os.getenv("MONGODB_PWD")

classification_uri = os.getenv("CLASSIFICATION_URI")
classification_port = os.getenv("CLASSIFICATION_PORT")
classification_route = os.getenv("CLASSIFICATION_ROUTE")

connect_to_database(uri, uname, pwd)
set_image_predictor(classification_uri, classification_port, classification_route)
# populate_db_recipes('data/raw/ArgentinianRecipes')
populate_db_images('data/raw/ArgentinianRecipes')
res = get_recipe_from_db(277888)
breakpoint()

# print(recipe_ids())
# sim_ctrl = SimilarityController()
# sim_ctrl_vis = SimilarityControllerVisitor()

# sim_ctrl_vis.visit(sim_ctrl, uniform_score)
# test = ["apple", "cinnamon", "walnut"]

# mask = sim_ctrl.handle(test, 5)


# Documentation for mongodb docker: https://hub.docker.com/_/mongo
