#!/usr/bin/env python3

from food_project.recipe.crf.cluster_bi_occurrences import cluster_df

def get_recipe_counts_with_both(ing1, ing2):
    '''Returns the number of recipes that contain both ing1 and ing2'''
    return sum(cluster_df.apply(lambda x: x[ing1] == 1 and x[ing2]==1, axis=1))

def get_number_of_recipes():
    return cluster_df.shape[0]
