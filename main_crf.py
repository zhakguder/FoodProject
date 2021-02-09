#!/usr/bin/env python3

# from food_project.recipe.crf import get_recipe_counts_with_both
# from food_project.image_classification.crf import get_class_clusters

# class_clusters = get_class_clusters()
# clusters = list(class_clusters.values())
# get_recipe_counts_with_both(clusters[0], clusters[1])

import os
from dotenv import load_dotenv
# from food_project.image_classification.crf import edge_potentials_dict, make_test_image
from food_project.image_classification import set_image_predictor, predict_image
from food_project.image_classification.crf.preprocess import read_image
# print(edge_potentials_dict)

# canvas = make_test_image('data/crf/test_images/raw', 3, write=True, path='data/crf/test_images/compiled/1.jpeg')
load_dotenv()
classification_type = "INGR"  # or DISH

classification_uri = os.getenv("SERVER_URI")
prefix = classification_type + "_CLASS_"
classification_port = os.getenv(prefix + "PORT")
classification_route = os.getenv(prefix + "ROUTE")



set_image_predictor(classification_uri, classification_port, classification_route)
grid_image_path = 'data/crf/test_images/compiled/1.jpeg'

grid_image = read_image(grid_image_path)
predict_image(grid_image, classification_type)
