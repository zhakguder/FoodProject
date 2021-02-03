#!/usr/bin/env python3

from food_project.recipe.similarity.entropy import __entropy, EntropyVisitor, EntropyClusterVisitor
from food_project.recipe.similarity.importance import ImportanceCalculator

def calculate_entropies(collection:list) -> dict:
    '''Calculates entropies for all the items in the collection. Entropy definition is taken from paper Complexity and Similarity of Recipes based on Entropy Measurement.
    Returns a dictionary of entries where each key is taken from collection.
    '''
    visitor = EntropyVisitor(collection)
    __entropy.accept(visitor)
    return __entropy.calculate()

def get_entropy_mask(df, n):
    '''Returns the n highest entropies in every recipe'''
    return __entropy.entropy_mask(df, n)
def get_item_entropy(item_name:str)->float:
    return __entropy.get_item_entropy(item_name)

# entropies = None

def entropy_update(collection):
    # global entropies
    entropies = calculate_entropies(collection)

def cluster_entropy_update(cluster_entropies):
    ecv = EntropyClusterVisitor(cluster_entropies)
    __entropy.accept(ecv)

def get_cluster_entropies():
    return __entropy.cluster_entropies

def calculate_importance(mask, mask_type='db_recipes'):
    ic = ImportanceCalculator()
    return ic.calculate_importances(mask, mask_type)
