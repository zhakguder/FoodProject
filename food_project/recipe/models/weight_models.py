#!/usr/bin/env python3
from functools import partial
from food_project.util import (
    column_name,
    column_value,
    dataframe_from_dict,
    dataframe_from_list,
    read_json,
    read_pickle,
    save_dataframe,
    series_from_dict,
)
from food_project.recipe.cluster import ingredient_clusters
from food_project.recipe.ingredient import Ingredient, IngredientCluster
from food_project.recipe.similarity import get_item_entropy


class RecipeModel:
    def __init__(self):
        self.filename = None
        self.scaled_ingredients = None

    # def _read_data(self):
    # self.scaled_ingredients = read_pickle(self.filename)

    def _recipe_percentage_normalize(self, df):
        row_totals = df.sum(axis=1)
        return df.div(row_totals, axis=0)

    def _get_ingredient_name(self, i):
        self._read_data()
        try:  # TODO: remove after abstract factory is implemented
            return partial(column_name, self.scaled_ingredients)(i)
        except:
            raise Exception("Not existent")

    def _get_ingredient_quantity(self, i):
        self._read_data()
        return partial(column_value, self.scaled_ingredients)(i)

    def _get_ingredient_entropy(self, ingredient_name: str) -> float:
        return get_item_entropy(ingredient_name)


class RecipeWeightIngredientModel(RecipeModel):
    def __init__(self):
        super().__init__()
        print("INIT WEIGHT INGREDIENT MODEL")
        # self.conversion_file = "data/recipes/all_weight_cup.json"
        self.conversion_file = "data/recipes/unit_conversion/new_corrected_meta.json"

    def _read_data(self):
        if self.scaled_ingredients is None:
            gram_data = read_json(self.conversion_file)
            columns = ["id", "name", "qty", "unit"]  # TODO
            tmp_df = dataframe_from_list(gram_data["data"], columns)
            # tmp_df = tmp_df[tmp_df["unit"] != "cup"]
            tmp_df = tmp_df.astype({"qty": "float", "id": "float"})
            tmp_df = tmp_df.drop_duplicates(subset=["id", "name"])
            tmp_df = tmp_df.pivot(index="id", columns="name", values="qty")
            tmp_df[tmp_df.isna()] = 0
            self.scaled_ingredients = tmp_df
            tmp = read_pickle(
                "data/recipes/recipe_ingredients_scaled_units_wide_df.pkl"
            )

            breakpoint()

    def get_data(self):
        self._read_data()


class RecipeWeightClusterModel(RecipeWeightIngredientModel):
    """Data after parsing raw recipes. Consolidated into clusters."""

    # TODO: Model should only load/save data, extract logic in this to a controller helper class
    def __init__(self):
        print("INIT WEIGHT CLUSTER MODEL")
        super().__init__()
        self.clusters = None
        self.is_clusters_formed = lambda: self.clusters is not None

    def _consolidate_clusters(self):
        clusters = []
        for k, v in ingredient_clusters.items():
            ingredients = []
            for i in v:

                try:  # TODO: remove after you have abstract factory class
                    name = self._get_ingredient_name(i)

                except:
                    print("name not found")
                    continue
                quantity = self._get_ingredient_quantity(i)
                entropy = self._get_ingredient_entropy(name)
                ingredients.append(Ingredient(name, i, quantity, entropy))

            ic = IngredientCluster(k, *ingredients)
            clusters.append(ic)
        return clusters

    def get_data(self):
        if not self.is_clusters_formed():
            clusters = self._consolidate_clusters()
        df = dataframe_from_dict(
            {x.name: x.get_quantity() for x in clusters}
        )  # TODO: This shouldn't depend on the availability of entropies
        return self._recipe_percentage_normalize(df)

    def export_cluster_df(self, path):
        df = self.get_data()
        save_dataframe(df, path)

    def get_entropy(self):
        if not self.is_clusters_formed():
            clusters = self._consolidate_clusters()
        return series_from_dict({x.name: x.get_entropy() for x in clusters})

    def get_amount_of_cluster_in_recipe(self, cluster_name, recipe_id):

        data = self.get_data()
        return data.loc[recipe_id, cluster_name]
