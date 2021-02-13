#!/usr/bin/env python3

from food_project.recipe.crf.cluster_bi_occurrences import cluster_df


def get_recipe_counts_containing_ingredients(*ings):
    """Returns the number of recipes that contain all ingredients in ings"""
    print(ings)
    ingrs_df = cluster_df[list(ings)]
    return ingrs_df.all(axis=1)


def get_number_of_recipes():
    return cluster_df.shape[0]
