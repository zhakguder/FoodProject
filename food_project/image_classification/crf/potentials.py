#!/usr/bin/env python3
import os
import pickle

from food_project.image_classification.crf.prediction_class_clusters import (
    get_class_clusters,
)
from food_project.recipe.crf import get_number_of_recipes, get_recipe_counts_with_both

# All names are in terms of clusters


def name_potential(node1, node2):
    return "+".join(sorted([node1, node2]))


class NodePotential:
    def __init__(self, name, cluster, potential):
        self.name = name
        self.cluster = cluster
        self._potential = potential

    @property
    def potential(self):
        return self._potential


class EdgePotentials:
    def __init__(self, path):
        class_clusters = get_class_clusters()
        self.clusters = list(class_clusters.values())
        self.n_total_recipes = get_number_of_recipes()
        self.edge_potentials = {}
        self.path = path  # This is ugly

    def _calculate_bi_frequencies(self):
        clusters = self.clusters
        for ci in clusters:
            for cj in clusters:
                name = name_potential(ci, cj)
                if name not in self.edge_potentials:
                    cnt = get_recipe_counts_with_both(ci, cj)
                    freq = cnt / self.n_total_recipes
                    self.edge_potentials[name_potential(ci, cj)] = freq
        return self.edge_potentials

    def _save_frequencies(self, frequencies):
        if not os.path.exists(self.path):
            with open(self.path, "wb") as f:
                pickle.dump(frequencies, f)

    def get_frequencies(self):
        if not os.path.exists(self.path):
            self.frequencies = self._calculate_bi_frequencies()
            self._save_frequencies(self.frequencies)
        else:
            with open(self.path, "rb") as f:
                self.frequencies = pickle.load(f)
        return self.frequencies

    def bi_frequency(self, c_i, c_j):
        self.get_frequencies()

        # TODO: is it good to keep this 1? This might be useful when we have
        # empty nodes to make it ineffective
        try:
            return self.edge_potentials[name_potential(c_i, c_j)]
        except:
            return 1


# class EdgePotential:
#     potentials = EdgePotentials()
#     def __init__(self, node1, node2):
#         self.node1 = node1
#         self.node2 = node2
#         self.name = name_potential(node1, node2)
#         self._potential = EdgePotential.potentials.bi_frequency(node1, node2)

#     @property
#     def potential(self):
#         return self._potential

_edge_potentials = EdgePotentials("data/crf/edge_potentials_dict.pkl")


def get_edge_potential(node1, node2):
    return _edge_potentials.bi_frequency(node1, node2)
