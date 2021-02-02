#!/usr/bin/env python3
import os

from functools import partial
from food_project.util import (
    read_pickle,
    column_name,
    column_value,
    dataframe_from_dict,
    series_from_dict,
    save_dataframe,
    read_json,
    list_content_with_matches,
    comparison,
)
from food_project.recipe.cluster import ingredient_clusters
from food_project.recipe.ingredient import Ingredient, IngredientCluster
from food_project.recipe.similarity import get_item_entropy

from pymongo import MongoClient


class QueryModel:
    def _set_data(self, ingredients):
        self.ingredients = ingredients

    def get_data(self, *ingredients):
        self._set_data(ingredients)
        return self.ingredients


# TODO: Change name to reflect that this is not a db model
#
#
class RecipeModel:
    def __init__(self):
        self.filename = "data/recipes/recipe_ingredients_scaled_units_wide_df.pkl"
        self.scaled_ingredients = None

    def _read_data(self):
        self.scaled_ingredients = read_pickle(self.filename)

    def _recipe_percentage_normalize(self, df):
        row_totals = df.sum(axis=1)
        return df.div(row_totals, axis=0)

    def _get_ingredient_name(self, i):
        if self.scaled_ingredients is None:
            self._read_data()
        return partial(column_name, self.scaled_ingredients)(i)

    def _get_ingredient_quantity(self, i):
        if self.scaled_ingredients is None:
            self._read_data()
        return partial(column_value, self.scaled_ingredients)(i)

    def _get_ingredient_entropy(self, ingredient_name: str) -> float:
        return get_item_entropy(ingredient_name)


class RecipeClusterModel(RecipeModel):
    """Data after parsing raw recipes. Consolidated into clusters."""

    # TODO: Model should only load/save data, extract logic in this to a controller helper class
    def __init__(self):
        super().__init__()
        self.clusters = None
        self.is_clusters_formed = lambda: self.clusters is not None
        self.normalized_data = None

    def _consolidate_clusters(self):
        clusters = []
        for k, v in ingredient_clusters.items():
            ingredients = []
            for i in v:
                name = self._get_ingredient_name(i)
                quantity = self._get_ingredient_quantity(i)
                entropy = self._get_ingredient_entropy(name)
                ingredients.append(Ingredient(name, i, quantity, entropy))

            ic = IngredientCluster(k, *ingredients)
            clusters.append(ic)
        return clusters

    def get_data(self):
        if not self.is_clusters_formed():
            clusters = self._consolidate_clusters()
        df = dataframe_from_dict({x.name: x.get_quantity() for x in clusters}) # TODO: This shouldn't depend on the availability of entropies
        self.normalized_data = self._recipe_percentage_normalize(df)
        return self.normalized_data

    def export_cluster_df(self, path):
        df = self.get_data()
        save_dataframe(df, path)
    def get_entropy(self):
        if not self.is_clusters_formed():
            clusters = self._consolidate_clusters()
        return series_from_dict({x.name: x.get_entropy() for x in clusters})
    def get_amount_of_cluster_in_recipe(self, cluster_name, recipe_id):
        if self.normalized_data is None:
            data = self.get_data()
        breakpoint()

class RecipeIngredientModel(RecipeModel):
    def __init__(self):
        super().__init__()

    def get_data(self):
        self._read_data()
        return self._recipe_percentage_normalize(self.scaled_ingredients)

    # def _calculate_ingredient_entropies(self):
    #     if self.scaled_ingredients is None:
    #         self._read_data()
    #     self.entropies = self.scaled_ingredients.copy()
    #     ingredients = self.scaled_ingredients.columns
    #     entropies = {}
    #     for ingredient in ingredients:
    #         entropies[ingredient] = get_item_entropy(ingredient)
    #     return entropies

    # def calculate_recipe_ingredient_entropies(self):
    #     entropies = self._calculate_ingredient_entropies()

    #     for colname in self.entropies.columns:
    #         values = self.entropies[colname]
    #         self.entropies[colname] = values.apply(lambda x: entropies[colname] if x > 0 else 0)
    #     return self.entropies


class RecipeDBInitiator:
    def __init__(self, uri, uname, pwd):
        self.db_uri = uri
        self.uname = uname
        self.pwd = pwd

    def visit(self, element):
        """Sets username and password for recipe database and establishes connection to database"""
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
        self.key_field = "recipe_ID"

    def _connect(self):
        client = MongoClient(self.uri)
        db = client["food"]
        self.collection = db["recipe"]

    def load(self, id_):
        id_ = str(id_)
        return self.collection.find_one({self.key_field: id_})

    def save(self, data):
        id = data["_id"]  # TODO: fix according to recipe class
        try:
            self.collection.insert_one(data)
            # print(f"Inserted recipe id {id}")
        except:
            # print(f"Couldn't insert recipe id {id}")
            pass

    def update(self, id_, data):
        """data: key value pair"""
        id_ = str(id_)
        try:
            updated = self.collection.find_one_and_update(
                {self.key_field: id_}, {"$set": data}, upsert=True
            )
            # print(f"Updated recipe id {id_}")

        except:
            # print(f"Couldn't update {id_}")
            pass
        return updated

    def _retrieve_all(self):
        return self.collection.find()

    def retrieve_field(self, field_name):
        coll = self._retrieve_all()
        field_val = lambda x: x.get(field_name, [])
        return [field_val(x) for x in coll]

    def accept(self, visitor):
        visitor.visit(self)


class RawRecipeReader:
    # TODO: factor out a recipe class with _id, etc
    def __init__(self):
        self._reset()

    def _reset(self):
        self.path = None
        self.data = None
        self._recipe_ids = None

    def read(self):
        """Returns recipe data in json format"""
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
        return [x for x in self.data if x["recipe_ID"] == recipe_id][0]

    def recipe_by_id(self, recipe_id):
        x = self._filter_by_id(recipe_id)
        x["_id"] = x["recipe_ID"]
        return x

    def accept(self, visitor):
        self._reset()
        visitor.visit(self)


class ProcessedRecipeReader:
    def __init__(self):
        self._reset()

    def _reset(self):
        self.path = None
        self.data = None
        self._recipe_id = None

    @property
    def ready(self):
        return self.data is not None

    def read(self):
        with open(self.path, "r") as f:
            self.data = [x.strip() for x in f.readlines()]
        return self.data

    @property
    def recipe_id(self):
        if not self._recipe_id:
            self._recipe_id = os.path.basename(self.path).split(".")[0]
        return self._recipe_id

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
        self.inner_dir = "original_recipes_info"
        self.suffix = "json"
        self.match_cond = comparison(str.endswith, self.suffix)


class ProcessedRecipeGroup(RawDataGroup):
    def __init__(self):
        super().__init__()
        self.suffix = "out"
        self.match_cond = comparison(str.endswith, self.suffix)


class RawRecipeImageGroup(RawDataGroup):
    def __init__(self):
        super().__init__()
        self.inner_dir = "imgs"
        self.match_cond = comparison(os.path.isdir)


class RawImageGroup(RawDataGroup):
    def __init__(self):
        super().__init__()
        self.suffix = "jpg"
        self.match_cond = comparison(str.endswith, self.suffix)


class RecipeFilePathSetter:
    def __init__(self, path):
        self.path = path

    def visit(self, element):
        element.path = self.path


raw_recipe_model = RawRecipeModel()
raw_recipe_reader = RawRecipeReader()
