#!/usr/bin/env python3

from food_project.recipe import SimilarityController, SimilarityControllerVisitor
from food_project.recipe.matcher import match_score, uniform_score
from food_project.recipe import rrm

# sim_ctrl = SimilarityController()
# sim_ctrl_vis = SimilarityControllerVisitor()

# sim_ctrl_vis.visit(sim_ctrl, uniform_score)
# test = ["apple", "cinnamon", "walnut"]

# mask = sim_ctrl.handle(test, 5)


# Documentation for mongodb docker: https://hub.docker.com/_/mongo
rrm.save()
