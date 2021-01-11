#!/usr/bin/env python3
import os

from bson.objectid import ObjectId
from functools import partial
from food_project.util import read_pickle, column_name, column_value, dataframe_from_dict, read_json, list_content_with_matches, comparison
from food_project.recipe.cluster import ingredient_clusters
from food_project.recipe.ingredient import Ingredient, IngredientCluster
from pymongo import MongoClient

class QueryModel:
    def _set_data(self, ingredients):
        self.ingredients = ingredients

    def get_data(self, *ingredients):
        self._set_data(ingredients)
        return self.ingredients

# TODO: Change name to reflect that this is not a db model
class RecipeModel:
    '''Data after parsing raw recipes. Consolidated into clusters.'''
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


class RawRecipeModel:
    def __init__(self):
        self.username = None
        self.password = None
        self.uri = None
        self.path = None
        self.key_field = 'recipe_ID'
    def _connect(self):
        client = MongoClient(self.uri)
        db = client['food']
        self.collection = db['recipe']

    def load(self, id_):
        id_ = str(id_)
        return self.collection.find_one({self.key_field: id_})

    def save(self, data):
        id = data['_id'] #TODO: fix according to recipe class
        try:
            self.collection.insert_one(data)
            print(f"Inserted recipe id {id}")
        except:
            print(f"Couldn't insert recipe id {id}")

    def update(self, id_, data):
        '''data: key value pair'''
        id_ = str(id_)
        try:
            updated = self.collection.find_one_and_update({self.key_field: id_}, {"$set": data}, upsert=True)
            print(f"Updated recipe id {id_}")
        except:
            print(f"Couldn't update {id_}")
        return updated

    def accept(self, visitor):
        visitor.visit(self)



class RawRecipeReader:
    #TODO: factor out a recipe class with _id, etc
    def __init__(self):
        self._reset()
    def _reset(self):
        self.path = None
        self.data = None
        self._recipe_ids = None


    def read(self):
        '''Returns recipe data in json format'''
        self.data = read_json(self.path)

    @property
    def ready(self):
        return self.data is not None
    @property
    def recipe_ids(self):
        if not self._recipe_ids:
            self._recipe_ids = [x["recipe_ID"] for x in self.data]
        return self._recipe_ids

    def _filter_by_id(self, recipe_id):
        return [x for x in self.data if x['recipe_ID']==recipe_id][0]

    def recipe_by_id(self, recipe_id):
        x = self._filter_by_id(recipe_id)
        x["_id"] = x['recipe_ID']
        # return {k:v for k,v in x.items() if k!='recipe_ID'}
        return x

    def accept(self, visitor):
        self._reset()
        visitor.visit(self)

class RawDataGroup:
    def __init__(self):
        self.path = None
        self.inner_dir = None
    def content_path(self):
        if self.inner_dir is not None:
            return os.path.join(self.path, self.inner_dir)
        else:
            return self.path

    def process(self):
        return list_content_with_matches(self.content_path(), self.match_cond)

    def accept(self, visitor):
        visitor.visit(self)

class RawRecipeGroup(RawDataGroup):
    def __init__(self):
        super().__init__()
        self.inner_dir = 'original_recipes_info'
        self.suffix = 'json'
        self.match_cond = comparison(str.endswith, self.suffix)

class ProcessedRecipeGroup(RawDataGroup):
    def __init__(self):
        super().__init__()
        self.suffix = 'out'
        self.match_cond = comparison(str.endswith, self.suffix)

class RawRecipeImageGroup(RawDataGroup):
     def __init__(self):
        super().__init__()
        self.inner_dir = 'imgs'
        self.match_cond = comparison(os.path.isdir)

class RawImageGroup(RawDataGroup):
    def __init__(self):
        super().__init__()
        self.suffix = 'jpg'
        self.match_cond = comparison(str.endswith, self.suffix)



class RecipeFilePathSetter:
    def __init__(self, path):
        self.path = path
    def visit(self, element):
        element.path = self.path


raw_recipe_model = RawRecipeModel()
raw_recipe_reader = RawRecipeReader()
