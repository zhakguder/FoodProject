#!/usr/bin/env python3

# from food_project.recipe.crf import get_recipe_counts_with_both
# from food_project.image_classification.crf import get_class_clusters

# class_clusters = get_class_clusters()
# clusters = list(class_clusters.values())
# get_recipe_counts_with_both(clusters[0], clusters[1])

from food_project.image_classification.crf import edge_potentials_dict

print(edge_potentials_dict)
