#!/usr/bin/env python3

import pickle
import pandas as pd
import json


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

def dataframe_from_dict(dict):
    return pd.DataFrame(dict)

def matching_columns(df, text):
    return df.columns.str.contains(text)
