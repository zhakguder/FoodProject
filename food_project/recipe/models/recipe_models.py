#!/usr/bin/env python3
from abc import ABC, abstractmethod
from food_project.recipe.models.volume_models import (
    RecipeClusterModel,
    RecipeIngredientModel,
)
from food_project.recipe.models.weight_models import (
    RecipeWeightClusterModel,
    RecipeWeightIngredientModel,
)


class RecipeModelAbstractFactory(ABC):
    @abstractmethod
    def create_ingredient_model(self):
        pass

    @abstractmethod
    def create_cluster_model(self):
        pass


class RecipeModelVolumeFactory(RecipeModelAbstractFactory):
    def create_ingredient_model(self):
        return RecipeIngredientModel()

    def create_cluster_model(self):
        return RecipeClusterModel()


class RecipeModelWeightFactory(RecipeModelAbstractFactory):
    def create_ingredient_model(self):
        return RecipeWeightIngredientModel()

    def create_cluster_model(self):
        return RecipeWeightClusterModel()
