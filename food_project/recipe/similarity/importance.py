#!/usr/bin/env python3
"""Currently, these classes are not used. Importance is calculated using recipe.recipe.Recipe class"""
from abc import ABC, abstractmethod


class ImportanceCalculator:
    def _create_ranker(self, mask_type):
        """Return an importance ranker"""
        if mask_type == "db_recipes":
            return DBRecipesRanker()
        else:
            return QueryRecipeRanker()

    def calculate_importances(self, mask, mask_type):
        ranker = self._create_ranker(mask_type)
        return ranker.get_ranks(mask)


class Ranker(ABC):
    @abstractmethod
    def get_ranks(self, values):
        pass


class QueryRecipeRanker(Ranker):
    def get_ranks(self, values):
        ranks = values.rank(ascending=False, method="dense")
        tmp = ranks[values != 0]
        return tmp


class DBRecipesRanker(Ranker):
    def get_ranks(self, values):
        # TODO: GO FROM HERE!
        tmp = values.rank(ascending=False, method="dense", axis=1)
