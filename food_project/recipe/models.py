#!/usr/bin/env python3
import os
from functools import partial
from food_project.util import read_pickle, column_name, column_value, dataframe_from_dict, read_json, list_files_with_suffix
from food_project.recipe.cluster import ingredient_clusters
from food_project.recipe.ingredient import Ingredient, IngredientCluster
from pymongo import MongoClient

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
        self.fname = None

    def _connect(self):
        client = MongoClient(self.uri)
        db = client['food']
        self.collection = db['recipe']

    def load(self, id):
        pass

    def save(self, entry=16836):
        try:
            data = read_json(self.fname)
        except Exception as e:
            raise e
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

class RawRecipeReader:
    def __init__(self):
        self._reset()
    def _reset(self):
        self.fname = None
        self.data = None
        self._recipe_ids = None


    def read(self):
        '''Returns recipe data in json format'''
        self.data = read_json(self.fname)

    @property
    def recipe_ids(self):
        if not self._recipe_ids:
            self._recipe_ids = [x["recipe_ID"] for x in self.data]
        return self._recipe_ids

    def accept(self, visitor):
        self._reset()
        visitor.visit(self)

class RawRecipeGroup:
    def __init__(self):
        self.path = None
        self.inner_dir = 'original_recipe_info'

    def process(self):
        path = os.path.join(self.path, self.inner_dir)
        return list_files_with_suffix(path, 'json')

    def accept(self, visitor):
        visitor.visit(self)

class RecipeFilePathSetter:
    def __init__(self, path):
        self.path = path
    def visit(self, element):
        element.fname = self.path
