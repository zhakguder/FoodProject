#!/usr/bin/env python3

from food_project.util import read_json

clusters = read_json('data/recipes/ingr_clusters.json')
cluster_ids = read_json('data/recipes/ingr_id_clusters.json')

# clusters has been consolidated for plural cluster names
# base words are removed from  cluster_ids
# intersection of both is clean

cluster_keys = clusters.keys() & cluster_ids.keys()
ingredient_clusters = {x: cluster_ids[x] for x in cluster_keys}
