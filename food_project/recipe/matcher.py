#!/usr/bin/env python3

import numpy as np
import pandas as pd


from food_project.util import matching_columns, match_score, uniform_score


class IngredientQuery:
    def __init__(self, *ingredients):
        self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        self.ingredients += ingredient

    @property
    def query(self):
        return "|".join(self.ingredients)


class IngredientMatcher:
    def __init__(self, recipe_collection, scoring_strategy):
        self.recipe_collection = recipe_collection
        self.match_scoring_strategy = scoring_strategy

    def _find_matching_cols(self, query):
        matched_cols = matching_columns(self.recipe_collection, query)
        return matched_cols

    def query_mask(self, ingredient_query):
        matched_cols = self._find_matching_cols(ingredient_query.query)
        mask = pd.Series(0, index=self.recipe_collection.columns, dtype=np.float)

        matched_cols_ = np.argwhere(matched_cols > 0).reshape(-1)
        n = len(matched_cols_)
        match_scores = list(
            map(
                self.match_scoring_strategy,
                self.recipe_collection.columns[matched_cols],
                [ingredient_query.query] * n,
            )
        )

        for i in range(n):
            mask[matched_cols_[i]] = match_scores[i]
        return mask
