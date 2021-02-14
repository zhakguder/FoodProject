#!/usr/bin/env python3
import os
import pickle

from food_project.image_classification.crf.prediction_class_clusters import \
    get_class_clusters
from food_project.recipe.crf import (get_number_of_recipes,
                                     get_recipe_counts_containing_ingredients)

# All names are in terms of clusters

class_clusters = get_class_clusters()
clusters = class_clusters.values()
n_clusters = clusters
id_clusters = {x[0]: x[1] for x in zip(range(len(n_clusters)), clusters)}
clusters_ids = {v: k for k, v in id_clusters.items()}


def name_potential(*nodes):
    node_ids = [str(clusters_ids[x]) for x in nodes]
    return "+".join(sorted(node_ids))


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
                    if len(set([ci, cj, ck])) != 3:
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
        print("get freq")
        if not os.path.exists(self.path):
            print("path doesnt exist")
            self._calculate_bi_frequencies()
            print("bi calc finished")
            self._calculate_tri_frequencies()
            print("tri calc finished")
            self._save_frequencies(self.clique_potentials)
        else:
            print("path exists")
            if not self.clique_potentials:
                with open(self.path, "rb") as f:
                    self.clique_potentials = pickle.load(f)
        return self.clique_potentials

    def clique_potential(self, *nodes):
        print("here")
        self.get_frequencies()

        # TODO: is it good to keep this 1? This might be useful when we have
        # empty nodes to make it ineffective
        try:
            print("there")
            return self.clique_potentials[name_potential(*nodes)]
        except:
            print("and there")
            return 1


_clique_potentials = CliquePotentials("data/crf/clique_potentials_dict.pkl")


def get_clique_potential(*nodes):
    return _clique_potentials.clique_potential(*nodes)
