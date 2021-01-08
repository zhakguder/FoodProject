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
        self.username = None
        self.password = None
        self.uri = None
        self.json_prefix = None

    def _connect(self):
        client = MongoClient(self.uri)
        db = client['food']
        self.collection = db['recipe']

    def load(self, id):
        pass

    def save(self, entry=16836):
        filename = f"{self.json_prefix}_{entry}.json"
        with open(filename, 'r')as f:
            data = json.load(f)
        try:
            self.collection.insert_one(data)
            print(f"Inserted recipe id {entry}")
        except:
            print(f"Couldn't insert recipe id {entry}")
    def accept(self, visitor):
        visitor.visit(self)

class RecipeDBInitiator:
    def __init__(self, uri, uname, pwd):
        self.db_uri = uri
        self.uname = uname
        self.pwd = pwd
    def visit(self, element):
        '''Sets username and password for recipe database and establishes connection to database'''
        element.username = self.uname
        element.password = self.pwd
        element.uri = f"mongodb://{self.uname}:{self.pwd}@{self.db_uri}"
        element._connect()

class RecipeFilePathSetter:
    def __init__(self, path):
        self.path = path
    def visit(self, element):
        element.json_prefix = self.path
