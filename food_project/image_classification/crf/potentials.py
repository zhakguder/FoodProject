#!/usr/bin/env python3
import os
import pickle
from food_project.recipe.crf import get_recipe_counts_with_both, get_number_of_recipes
from food_project.image_classification.crf.prediction_class_clusters import get_class_clusters


def name_potential(node1, node2):
    return "+".join(sorted([node1, node2]))


class NodePotential:
    def __init__(self, name, potential):
        self.name = name
        self._potential = potential

    @property
    def potential(self):
        return self._potential


class EdgePotential:
    def __init__(self, potential, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self._potential = potential
        self.name = name_potential(node1, node2)

    @property
    def potential(self):
        return self._potential

class EdgePotentials:
    def __init__(self, path):
        class_clusters = get_class_clusters()
        self.clusters = list(class_clusters.values())
        self.n_total_recipes = get_number_of_recipes()
        self.edge_potentials = {}
        self.path = path # This is ugly

    def _calculate_bi_frequencies(self):
        clusters = self.clusters
        for ci in clusters:
            for cj in clusters:
                cnt = get_recipe_counts_with_both(ci, cj)
                freq = cnt/self.n_total_recipes
                self.edge_potentials[name_potential(ci, cj)] = freq
        return self.edge_potentials
    def _save_frequencies(self, frequencies):
        if not os.path.exists(self.path):
            with open(self.path, 'wb') as f:
                pickle.dump(frequencies, f)

    def get_frequencies(self):
        if not os.path.exists(self.path):
            self.frequencies = self._calculate_bi_frequencies()
            self._save_frequencies(self.frequencies)
        else:
            with open(self.path, 'rb') as f:
                self.frequencies = pickle.load(f)
        return self.frequencies
