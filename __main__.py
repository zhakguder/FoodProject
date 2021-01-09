#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from food_project.recipe import SimilarityController, SimilarityControllerVisitor
from food_project.recipe.matcher import match_score, uniform_score
from food_project.recipe import connect_to_database, recipe_ids, RawRecipeGroup, set_recipe_group_dirname, set_recipe_reader_fname, list_recipe_files

load_dotenv()
uri = os.getenv("MONGODB_URI")
uname = os.getenv("MONGODB_USERNAME")
pwd = os.getenv("MONGODB_PWD")

# connect_to_database(uri, uname, pwd)
# read_recipe('MexicanBread/MexicanBread_16836.json')

rcg = RawRecipeGroup()
set_recipe_group_dirname('data/raw/ArgentinianRecipes', rcg)
for recipe_file in list_recipe_files(rcg):
    set_recipe_reader_fname(recipe_file)
    ids = recipe_ids()
    for id_ in ids:
        recipe = recipe_from_json_by_id(rcg, id_)
        print(recipe)


# print(recipe_ids())
# sim_ctrl = SimilarityController()
# sim_ctrl_vis = SimilarityControllerVisitor()

# sim_ctrl_vis.visit(sim_ctrl, uniform_score)
# test = ["apple", "cinnamon", "walnut"]

# mask = sim_ctrl.handle(test, 5)


# Documentation for mongodb docker: https://hub.docker.com/_/mongo
