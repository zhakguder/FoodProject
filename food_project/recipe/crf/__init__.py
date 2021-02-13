#!/usr/bin/env python3

from food_project.recipe.crf.cluster_bi_occurrences import cluster_df


def get_recipe_counts_containing_ingredients(*ings):
    """Returns the number of recipes that contain both ing1 and ing2"""

    ingrs_df = cluster_df[list(ings)]
    print(ingrs_df)
    res = sum(ingrs_df.all(axis=1))
    # res = sum(cluster_df.apply(lambda x: x[ings[0]] == 1 and x[ings[1]] == 1, axis=1))
    print(res)
    return res


def get_number_of_recipes():
    return cluster_df.shape[0]
