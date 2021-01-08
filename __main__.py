#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from food_project.recipe import SimilarityController, SimilarityControllerVisitor
from food_project.recipe.matcher import match_score, uniform_score
from food_project.recipe import connect_to_database, set_recipe_file_pathprefix

env = load_dotenv()
uri = os.getenv("MONGODB_URI")
uname = os.getenv("MONGODB_USERNAME")
pwd = os.getenv("MONGODB_PWD")

rrm = connect_to_database(uri, uname, pwd)
rrm = set_recipe_file_pathprefix('MexicanBread/MexicanBread')
# sim_ctrl = SimilarityController()
# sim_ctrl_vis = SimilarityControllerVisitor()

# sim_ctrl_vis.visit(sim_ctrl, uniform_score)
# test = ["apple", "cinnamon", "walnut"]

# mask = sim_ctrl.handle(test, 5)


# Documentation for mongodb docker: https://hub.docker.com/_/mongo
rrm.save()
