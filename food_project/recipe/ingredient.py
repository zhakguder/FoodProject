#!/usr/bin/env python3


class Ingredient:
    def __init__(self, name, id, quantity, entropy):
        self.name = name
        self.id = id  # column number in recipe ingredients dataframe
        self.quantity = quantity
        self.entropy = entropy


# clusters = {}
ingredients_to_clusters = {}  # TODO: put this into mongo
# TODO: separate populating this into an independent task, do it upfront once
# not with every run of the program


class IngredientCluster:
    def __init__(self, name, *ingredients):
        self.name = name
        self.ingredients = ingredients
        # self.quantity = 0
        # clusters[name] = self
        self.save_ingredients()  # TODO: functions shouldn't have side-effects!!!

    def save_ingredients(self):
        # TODO: not written well
        for ingredient in self.ingredients:
            ingredients_to_clusters[ingredient.name] = self.name

    def add_ingredient(self, ingredient):
        self.ingredients += (ingredient,)

    def get_quantity(self):
        # self.quantity = sum([x.quantity for x in self.ingredients])
        # return self.quantity
        return sum([x.quantity for x in self.ingredients])

    def get_entropy(self):
        # self.entropy =  sum([x.entropy for x in self.ingredients])
        # return self.entropy
        try:
            print("individual entropies:")
            n_ingredients = len([x for x in self.ingredients if x.entropy != 0])
            return sum([x.entropy for x in self.ingredients]) / n_ingredients
        except:
            return 0

    @staticmethod
    def ingredient_in_cluster(ing_name):
        # return [
        #     cluster.name for _, cluster in clusters if ing_name in cluster.ingredients
        # ]
        return ingredients_to_clusters.get(ing_name, None)
