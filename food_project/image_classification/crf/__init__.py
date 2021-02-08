#!/usr/bin/env python3
from food_project.image_classification.crf.potentials import EdgePotentials
from food_project.image_classification.crf.test import make_test_image

edge_potentials = EdgePotentials('data/crf/edge_potentials_dict.pkl')
edge_potentials_dict = edge_potentials.get_frequencies()
