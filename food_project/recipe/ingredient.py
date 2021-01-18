#!/usr/bin/env python3


class Ingredient:
    def __init__(self, name, id, quantity):
        self.name = name
        self.id = id  # column number in recipe ingredients dataframe
        self.quantity = quantity

clusters = {}


class IngredientCluster:
    def __init__(self, name, *ingredients):
        self.name = name
        self.ingredients = ingredients
        self.quantity = 0
        clusters[name] = self
    def add_ingredient(self, ingredient):
        self.ingredients += (ingredient,)

    def get_quantity(self):
        self.quantity = sum([x.quantity for x in self.ingredients])
        return self.quantity
    @staticmethod
    def ingredient_in_cluster(ing_name):
        return [cluster.name for _, cluster in clusters if ing_name in cluster.ingredients]
