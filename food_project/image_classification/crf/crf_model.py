#!/usr/bin/env python3
import itertools
import math

import numpy as np

from food_project.image_classification.crf.potentials import (
    NodePotential, get_clique_potential)
from food_project.image_classification.crf.prediction_class_clusters import \
    ClassCandidates


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
        # while len(self.nodes) < self.n:
        #     self.nodes.append([NodePotential("empty", 'empty', 1)])
        self.nodes = [
            x for x in self.nodes if x[0].name != "empty"
        ]  # this is hardcoded but is correct, when the image is empty in the grid, classifier returns {'empty':1} as response
        comb_2 = itertools.combinations(self.nodes, 2)
        comb_3 = itertools.combinations(self.nodes, 3)

        def adjusted_powerset(it):
            yield from chain.from_iterable(combinations(it, r) for r in range(2, 4))

        self.all_possible_configs = adjusted_powerset(self.nodes)

    def get_edge_potential(self, node1: str, node2: str):
        return get_clique_potential(node1, node2)

    def calc_setting_prob(self, setting):

        edge_probs = []
        node_probs = []
        n = len(setting)
        for i in range(n):
            node1 = setting[i]
            print(node1)
            node_probs.append(node1.potential)
            for j in range(i + 1, n):
                node2 = setting[j]
                if node1.name != node2.name:
                    print("in")
                    edge_probs.append(self.get_edge_potential(node1.name, node2.name))
        return np.sum(np.log(edge_probs)) + np.sum(np.log(node_probs))

    def get_node_config(self):
        for nt in self.all_possible_configs:
            print(nt)
            for prd in itertools.product(*nt):
                print(prd)
                yield prd

        # return next(self.all_possible_configs)

    def filter_at_threshold(self, threshold):
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            if node[0].potential >= threshold:
                self.nodes[i] = [node[0]]

    def get_best_config(self, threshold):
        self.make_full()
        self.filter_at_threshold(threshold)
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
