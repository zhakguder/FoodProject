#!/usr/bin/env python3
from food_project.image_classification.crf.prediction_classes import classes
from food_project.image_classification.crf.recipe_cluster_names import cluster_names
from food_project.util import clean_word, matchsubstring


word_separator = "_"


def get_cluster_names():
    return cluster_names


def get_ingredient_name_separator():
    return word_separator


def get_prediction_class_list():

    classes = _get_prediction_class_list()
    unwanted_words = _get_unwanted_words()

    for i, cls in enumerate(classes):
        cls_original = cls
        for word in unwanted_words:
            cls = clean_word(cls, word)
        if cls != cls_original:
            classes[i] = cls
    return classes


def _get_prediction_class_list():
    return classes


def _get_unwanted_words():
    return ["fruit", "fresh"]



def get_cluster_of_ingredient(ingredient):
    cluster_names = get_cluster_names()
    clusters = []
    words = ingredient.split(word_separator)
    max_score = 0
    cluster = ""
    for cluster_name in cluster_names:
        score = matchsubstring(cluster_name, ingredient)

        if score > max_score:
            max_score = score
            cluster = cluster_name

    return cluster


def get_class_clusters():
    prediction_classes = get_prediction_class_list()
    class_clusters = {}

    for cls in prediction_classes:
        cluster = get_cluster_of_ingredient(cls)
        class_clusters[cls] = cluster
    return class_clusters
