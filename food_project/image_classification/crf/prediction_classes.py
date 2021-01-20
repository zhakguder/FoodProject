#!/usr/bin/env python3

import pickle

class_file = "data/image_classification/hyvee_label.dict"


with open(class_file, "rb") as f:
    classes = pickle.load(f)
    classes = list(classes.keys())
