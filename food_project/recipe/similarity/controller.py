#!/usr/bin/env python3
from food_project.recipe.matcher import IngredientQuery, match_score, IngredientMatcher
from food_project.recipe.models import (
    QueryModel,
    RecipeClusterModel,
    RecipeIngredientModel,
)
from food_project.recipe.ingredient import IngredientCluster
from food_project.recipe.similarity import (
    get_entropy_mask,
    cluster_entropy_update,
    calculate_importance
)  # update cluster entropies in main this is not good


class SimilarityController:
    def __init__(self):
        self.query_model = QueryModel()
        self.recipe_cluster_model = RecipeClusterModel()
        self.recipe_ingredient_model = RecipeIngredientModel()
        self.scoring_strategy = match_score
        self.scaled_cluster_ingredients = None
        self.scaled_ingredients = None
        self.n_clusters_in_recipe = 0
        self.loaded = (
            lambda: self.scaled_cluster_ingredients is not None
            and self.scaled_ingredients is not None
        )

    def handle(self, request, n):
        """Calculates similarities using mask and the scaled_cluster_ingredients df.
            Returns ids and similarity scores of the top n most similar recipes.
        """
        if not self.loaded():
            self.load_data()

        cluster_entropy_update(self.recipe_cluster_entropies)  # this is not good here
        mask = self._get_mask(request)
        similarity_scores = self._get_similarity_scores(mask,self.n_clusters_in_recipe)
        self.recipe_ingredient_importance()
        return self._get_n_most_similar(similarity_scores, n)

    def recipe_ingredient_importance(self):
        calculate_importance(self.scaled_cluster_ingredients)
    def load_data(self):
        self.scaled_cluster_ingredients = self.recipe_cluster_model.get_data()
        breakpoint()
        self.scaled_ingredients = self.recipe_ingredient_model.get_data()
        self.recipe_cluster_entropies = self.recipe_cluster_model.get_entropy()
        self.loaded_flag = True

    def _get_mask(self, request):
        matcher = IngredientMatcher(
            self.scaled_cluster_ingredients, self.scoring_strategy
        )
        query_ingredients = self.query_model.get_data(*request)
        # TODO use IngredientCluster.ingredient_in_cluster to get relevant clusters for all ingredients
        # TODO you have to run this on pandas to get access to images
        clusters = []
        for ingredient in query_ingredients:
            cluster = IngredientCluster.ingredient_in_cluster(
                "_".join(ingredient.split(" "))
            )
            if cluster:
                clusters.append(cluster)

        self.n_clusters_in_recipe = len(set(clusters))
        entropy_mask = get_entropy_mask(
            self.scaled_cluster_ingredients, self.n_clusters_in_recipe
        )
        test = IngredientQuery(*query_ingredients)
        mask = matcher.query_mask(test)
        mask = mask * entropy_mask
        calculate_importance(mask)
        #TODO add importance ranking
        return mask

    def _get_similarity_scores(self, mask, n):
        ingredient_similarity_scores = mask * self.scaled_cluster_ingredients
        non_0_cnts = ingredient_similarity_scores.apply(lambda x: len(x[x!=0]), axis=1)
        rng = non_0_cnts.between(n-2, n+2)
        return ingredient_similarity_scores[rng].sum(axis=1)

    def _get_n_most_similar(self, arr, n):
        return arr.sort_values(ascending=False).iloc[:n]

    def accept(self, visitor):
        visitor.visit(self)


class SimilarityControllerVisitor:
    def __init__(self, scoring):
        self.scoring = scoring

    def visit(self, element):
        element.scoring_strategy = self.scoring
