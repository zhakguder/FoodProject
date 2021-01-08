#!/usr/bin/env python3
'''This module accumulates single ingredient quantities into cluster
quantitites. Resulting data is stored in a dataframe.'''

from food_project.util import read_pickle, column_name, column_value, dataframe_from_dict
from food_project.recipe.cluster import ingredient_clusters
from food_project.recipe.ingredient import Ingredient, IngredientCluster
from functools import partial

scaled_ingredients = read_pickle('data/recipe_ingredients_scaled_units_wide_df.pkl')
ingredient_name = partial(column_name, scaled_ingredients)
ingredient_quantity = partial(column_value, scaled_ingredients)

clusters = []
for k, v in ingredient_clusters.items():
    ingredients = [Ingredient(ingredient_name(i),i,ingredient_quantity(i)) for i in v]
    ic = IngredientCluster(k, *ingredients)
    clusters.append(ic)


scaled_cluster_ingredients = dataframe_from_dict({x.name: x.get_quantity() for x in clusters})
