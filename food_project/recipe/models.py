#!/usr/bin/env python3
from food_project.util import read_pickle, column_name, column_value, dataframe_from_dict
from food_project.recipe.cluster import ingredient_clusters
from food_project.recipe.ingredient import Ingredient, IngredientCluster
from functools import partial
from pymongo import MongoClient
import json


class QueryModel:
    def _set_data(self, ingredients):
        self.ingredients = ingredients

    def get_data(self, *ingredients):
        self._set_data(ingredients)
        return self.ingredients


class RecipeModel:
    # TODO: Model should only load/save data, extract logic in this to a controller helper class
    def __init__(self):
        self.filename = 'data/recipe_ingredients_scaled_units_wide_df.pkl'
        self.scaled_ingredients = None

    def get_data(self):
        clusters = self._consolidate_clusters()
        df = dataframe_from_dict({x.name: x.get_quantity() for x in clusters})
        return self._recipe_percentage_normalize(df)

    def _get_ingredient_name(self):
        if self.scaled_ingredients is None:
            self._read_data()
        return partial(column_name, self.scaled_ingredients)

    def _get_ingredient_quantity(self):
        if self.scaled_ingredients is None:
            self._read_data()
        return partial(column_value, self.scaled_ingredients)

    def _consolidate_clusters(self):
        clusters = []
        for k, v in ingredient_clusters.items():
            ingredients = [Ingredient(
                            self._get_ingredient_name()(i), i, self._get_ingredient_quantity()(i))
                            for i in v]
            ic = IngredientCluster(k, *ingredients)
            clusters.append(ic)
        return clusters

    def _read_data(self):
        self.scaled_ingredients = read_pickle(self.filename)

    def _recipe_percentage_normalize(self, df):
        row_totals = df.sum(axis=1)
        return df.div(row_totals, axis=0)


class RawRecipeModel:
   def __init__(self):
       # self.client = MongoClient('localhost', 27017)
       username = "root"
       password = "example"
       uri = "mongodb://root:example@sbbi-panda.unl.edu:27017"
       client = MongoClient(uri)
       # client = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
       db = client['food']
       self.collection = db['recipe']

   def load(self, id):
       pass

   def save(self, entry=16836):
       filename = 'MexicanBread/MexicanBread_{}.json'.format(
           entry)
       with open(filename, 'r')as f:
           data = json.load(f)

       self.collection.insert_one(data)
