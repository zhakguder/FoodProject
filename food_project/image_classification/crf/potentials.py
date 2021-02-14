#!/usr/bin/env python3
import os
import pickle

from food_project.image_classification.crf.prediction_class_clusters import \
    get_class_clusters
from food_project.recipe.crf import (get_number_of_recipes,
                                     get_recipe_counts_containing_ingredients)

# All names are in terms of clusters


def name_potential(*nodes):
    return "+".join(sorted(nodes))


class NodePotential:
    def __init__(self, name, cluster, potential):
        self.name = name
        self.cluster = cluster
        self._potential = potential

    @property
    def potential(self):
        return self._potential


class CliquePotentials:
    def __init__(self, path):
        class_clusters = get_class_clusters()
        self.clusters = list(class_clusters.values())
        self.n_total_recipes = get_number_of_recipes()
        self.clique_potentials = {}
        self.path = path  # This is ugly

        self.bi_freq = None
        self.tri_freq = None

    def _calculate_bi_frequencies(self):
        """Calculates cliques of size 2 and 3."""
        clusters = self.clusters
        for ci in clusters:
            for cj in clusters:
                name = name_potential(ci, cj)
                if ci == cj:
                    continue
                if name not in self.clique_potentials:
                    cnt = get_recipe_counts_containing_ingredients(ci, cj)
                    freq = cnt / self.n_total_recipes
                    self.clique_potentials[name] = freq
        return self.clique_potentials

    def _calculate_tri_frequencies(self):
        clusters = self.clusters
        for ci in clusters:
            for cj in clusters:
                for ck in clusters:
                    if len(set(ci, cj, ck)) > 1:
                        continue
                    name = name_potential(ci, cj, ck)
                    if name not in self.clique_potentials:
                        cnt = get_recipe_counts_containing_ingredients(ci, cj, ck)
                        freq = cnt / self.n_total_recipes
                        self.clique_potentials[name] = freq
        return self.clique_potentials

    def _save_frequencies(self, frequencies):
        if not os.path.exists(self.path):
            with open(self.path, "wb") as f:
                pickle.dump(frequencies, f)

    def get_frequencies(self):
        print("A")
        if not os.path.exists(self.path):
            print("B")
            self._calculate_bi_frequencies()
            self._calculate_tri_frequencies()
            print(clique_potentials)
            self._save_frequencies(self.clique_potentials)
        else:
            print("C")
            with open(self.path, "rb") as f:
                self.clique_potentials = pickle.load(f)
        return self.clique_potentials

    def clique_potential(self, *nodes):
        self.get_frequencies()

        # TODO: is it good to keep this 1? This might be useful when we have
        # empty nodes to make it ineffective
        try:
            return self.clique_potentials[name_potential(*nodes)]
        except:
            return 1


_clique_potentials = CliquePotentials("data/crf/clique_potentials_dict.pkl")


def get_clique_potential(*nodes):
    print(nodes)
    return _clique_potentials.clique_potential(*nodes)
