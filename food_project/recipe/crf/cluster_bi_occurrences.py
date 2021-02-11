#!/usr/bin/env python3

"""This module implements functions and classes to calculate pairwise ingredient
co-occurrences. Ingredients are represented by the cluster names they belong to.
Only the classes that will be used in image classification will be counted."""

from food_project.recipe import load_cluster_df

cluster_df = load_cluster_df("data/recipes/cluster_ingredients.df")
cluster_df[cluster_df > 0] = 1
