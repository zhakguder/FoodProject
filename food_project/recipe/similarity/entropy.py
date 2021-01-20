import pandas as pd
import numpy as np
import math


class Entropy:
    def __init__(self):
        self.collection = []
        self.freqs = {}
        self.ingredient_entropies = None
        self.cluster_entropies = None
        self.ranked_cluster_entropies = None
        self.ranked_ingredient_entropies = None

    def get_item_entropy(self, item_name: str) -> float:
        if not self.freqs:
            raise NameError("Frequencies not calculated.")
        return abs(
            -math.log10(self.freqs.get(item_name, 1))
        )  # abs to fix log10(1) = -0

    def calculate(self):
        if not self.freqs:
            collection = pd.Series(self.collection)
            counts = collection.value_counts()
            freqs = counts / self.n_collection

            self.ingredient_entropies = -np.log10(freqs)
            self.freqs = freqs.to_dict()
        return self.freqs

    def _rank_ingredient_entropies(self):
        self.ranked_ingredient_entropies = self.ingredient_entropies.rank(
            method="max", ascending=False
        )

    def _rank_cluster_entropies(self, df):
        df[df != 0] = 1
        df = df * self.cluster_entropies
        if self.cluster_entropies is not None:
            self.ranked_cluster_entropies =  df.rank(axis=1,  ascending=False)
        else:
            raise Exception("Cluster entropies are not calculated.")

    def entropy_mask(self, df, n):
        """Only keeps the ingredients with n highest entropies in each recipe"""
        # if self.ranked_ingredient_entropies is None:
        #     self._rank_ingredient_entropies()
        if self.ranked_cluster_entropies is None:
            self._rank_cluster_entropies(df.copy())
        res = self.ranked_cluster_entropies[self.ranked_cluster_entropies < n].fillna(0)
        # res[res != 0] = 1
        return res

    def accept(self, visitor):
        visitor.visit(self)


class EntropyVisitor:
    def __init__(self, collection: list) -> None:
        self.n_collection = len(collection)
        collection = [item for sublist in collection for item in sublist]
        self.collection = collection

    def visit(self, element):
        element.collection = self.collection
        element.n_collection = self.n_collection


class EntropyClusterVisitor:
    def __init__(self, clusters_entropy_df):
        self.cluster_entropies = clusters_entropy_df

    def visit(self, element):
        element.cluster_entropies = self.cluster_entropies


__entropy = Entropy()
