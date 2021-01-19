import pandas as pd
import numpy as np
import math


class Entropy:
    def __init__(self):
        self.collection = []
        self.freqs = {}
        self.entropies = None
        self.ranked_recipe_entropies = None
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

            self.entropies = -np.log10(freqs)
            self.freqs = freqs.to_dict()
        return self.freqs

    def _rank_entropies(self):
        self.ranked_ingredient_entropies = self.entropies.rank(
            method="max", ascending=False
        )

    def _rank_recipe_entropies(self, recipe_df):
        breakpoint()
        self.ranked_recipe_entropies = None

    def entropy_mask(self, df, n):
        """Only keeps the ingredients with n highest entropies in each recipe"""
        if self.ranked_ingredient_entropies is None:
            self._rank_entropies()
        if self.ranked_recipe_entropies is None:
            self._rank_recipe_entropies(df)
        print("A")
        res = self.ranked_recipe_entropies[self.ranked_recipe_entropies < n].fillna(0)
        res[res != 0] = 1
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


__entropy = Entropy()
