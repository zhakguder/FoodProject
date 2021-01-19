#!/usr/bin/env python3

from food_project.recipe.similarity.entropy import __entropy, EntropyVisitor

def calculate_entropies(collection:list) -> dict:
    '''Calculates entropies for all the items in the collection. Entropy definition is taken from paper Complexity and Similarity of Recipes based on Entropy Measurement.
    Returns a dictionary of entries where each key is taken from collection.
    '''
    visitor = EntropyVisitor(collection)
    __entropy.accept(visitor)
    return __entropy.calculate()

def get_entropy_mask(n):
    '''Returns the n highest entropies in every recipe'''
    breakpoint()
    return __entropy.entropy_mask(n)
def get_item_entropy(item_name:str)->float:
    return __entropy.get_item_entropy(item_name)

entropies = None

def entropy_update(collection):
    global entropies
    entropies = calculate_entropies(collection)
