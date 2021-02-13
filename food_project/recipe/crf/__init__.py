#!/usr/bin/env python3

from food_project.recipe.crf.cluster_bi_occurrences import cluster_df


def get_recipe_counts_containing_ingredients(*ings):
    """Returns the number of recipes that contain both ing1 and ing2"""

    print(cluster_df[ings])
    res = sum(cluster_df.apply(lambda x: x[ings[0]] == 1 and x[ings[1]] == 1, axis=1))
    return res


def get_number_of_recipes():
    return cluster_df.shape[0]
