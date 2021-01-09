#!/usr/bin/env python3

import pickle
import pandas as pd
import json
import os


def read_json(path):
    with open(path, 'r') as f:
        content =  json.load(f)
    return content

def read_pickle(path):
    with open(path, 'rb') as f:
        content = pickle.load(f)
    return content
def column_name(df, i):
    return df.columns[i]

def column_value(df, i):
    return df.iloc[:, i]

def dataframe_from_dict(mydict):
    return pd.DataFrame(mydict)

def matching_columns(df, text):
    return df.columns.str.contains(text)

def list_files_with_suffix(path, suffix):
    path = os.path.join(os.getcwd(), path)
    return [x for x in os.listdir(path) if x.endswith(suffix)]
