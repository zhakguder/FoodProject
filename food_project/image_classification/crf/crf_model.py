#!/usr/bin/env python3
import math
import numpy as np
import itertools
from food_project.image_classification.crf.potentials import (
    NodePotential,
    get_edge_potential,
)
from food_project.image_classification.crf.prediction_class_clusters import (
    ClassCandidates,
)


class CRF:
    def __init__(self, n: int, k: int) -> None:
        """Args:

        n: Number of nodes in CRF
        k: Number of variable values to consider for
        each node. Top k values for each node is considered.
        """
        self.n = n
        self.k = k
        self.nodes = []
        self.edges = {}
        self.all_possible_configs = None

    def add_node(self, node: ClassCandidates):
        clusters_probs = node.top_n_clusters(self.k)
        node = [NodePotential(x[0], x[1], x[2]) for x in clusters_probs]
        self.nodes.append(node)

    def make_full(self):
        while len(self.nodes) < self.n:
            self.nodes.append([NodePotential("empty", "empty", 1)])
        self.all_possible_configs = itertools.product(*self.nodes)

    def get_edge_potential(self, node1: str, node2: str):
        return get_edge_potential(node1, node2)

    def calc_setting_prob(self, setting):

        edge_probs = []
        node_probs = []
        n = len(setting)
        for i in range(n):
            node1 = setting[i]
            node_probs.append(node1.potential)
            for j in range(i + 1, n):
                node2 = setting[j]
                if node1 != node2:
                    edge_probs.append(self.get_edge_potential(node1.name, node2.name))

        return np.sum(np.log(edge_probs)) + np.sum(np.log(node_probs))

    def get_node_config(self):
        return next(self.all_possible_configs)

    def get_best_config(self):
        max_prob = -math.inf
        best_setting = None
        while True:
            try:
                setting = self.get_node_config()
            except StopIteration:
                break
            res = self.calc_setting_prob(setting)
            if res > max_prob:
                max_prob = res
                best_setting = setting
        best_setting = [x.name for x in best_setting if x.name != "empty"]
        return max_prob, best_setting


# TODO: KeyError: 'naan_breads+pineapple'
# TODO: fix some ingredients to given choice, so we don't try all possible combinations
