#!/usr/bin/env python3
from food_project.image_classification.crf.potentials import EdgePotentials

edge_potentials = EdgePotentials('data/image_classification/edge_potentials_dict.pkl')
edge_potentials_dict = edge_potentials.get_frequencies()
