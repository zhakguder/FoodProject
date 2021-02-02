#!/usr/bin/env python3
from food_project.recipe.ingredient import IngredientCluster
from food_project.recipe.similarity import get_cluster_entropies
from food_project.recipe.models import RecipeClusterModel

class Recipe:
    def __init__(self, id_, *ingredients):
        self.id_ = id_
        self.ingredients = ingredients
        self.cluster_entropies = get_cluster_entropies()
        self.clusters = [self._cluster_of_ingredient(x) for x in self.ingredients]
        self.cluster_amounts_model = RecipeClusterModel()

    def _cluster_of_ingredient(self, ingredient):
        return IngredientCluster.ingredient_in_cluster(ingredient)

    def _amount_of_cluster_of_ingredient(self, ingredient):
        cluster = self._cluster_of_ingredient(ingredient)
        return self.cluster_amounts_model.get_amount_of_cluster_in_recipe(cluster, float(self.id_))


    def importance_ranked_ingredients(self):
        ingredient_ranks = []
        for ing in self.ingredients:
            try:
                res = self._amount_of_cluster_of_ingredient(ing)
            except:
                continue
            ingredient_ranks.append(ing, res)
        breakpoint()
        print(ing,res)