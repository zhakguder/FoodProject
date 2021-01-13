#!/usr/bin/env python3
from food_project.recipe.matcher import (IngredientQuery, match_score,
                                         IngredientMatcher)
from food_project.recipe.models import QueryModel, RecipeModel


class SimilarityController:
    def __init__(self):
        self.query_model = QueryModel()
        self.recipe_model = RecipeModel()
        self.scoring_strategy = match_score

    def handle(self, request, n):
        '''Calculates similarities using mask and the scaled_cluster_ingredients df.
            Returns ids and similarity scores of the top n most similar recipes.
        '''
        self.scaled_cluster_ingredients = self.recipe_model.get_data()
        mask = self._get_mask(request)
        similarity_scores = self._get_similarity_scores(mask)
        return self._get_n_most_similar(similarity_scores, n)

    def _get_mask(self, request):
        matcher = IngredientMatcher(
                                self.scaled_cluster_ingredients,
                                self.scoring_strategy)
        query_ingredients = self.query_model.get_data(*request)
        test = IngredientQuery(*query_ingredients)
        mask = matcher.query_mask(test)
        return mask

    def _get_similarity_scores(self, mask):
        ingredient_similarity_scores = mask * self.scaled_cluster_ingredients
        breakpoint()
        return ingredient_similarity_scores.sum(axis=1)

    def _get_n_most_similar(self, arr, n):
        return arr.sort_values(ascending=False).iloc[:n]

    def accept(self, visitor):
        visitor.visit(self)


class SimilarityControllerVisitor:
    def __init__(self, scoring):
        self.scoring = scoring
    def visit(self, element):
        element.scoring_strategy = self.scoring
