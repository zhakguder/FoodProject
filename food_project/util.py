#!/usr/bin/env python3

import pickle
import pandas as pd
import json
import os

from functools import partial

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

# def list_files_with_suffix(path, suffix):
#     return [os.path.join(path, x) for x in os.listdir(path) if x.endswith(suffix)]

def _content_matches(path, match_cond):
    return match_cond.match(path)

def list_content_with_matches(path, match_cond):
    contents = os.listdir(path)
    return [os.path.join(path, x) for x in contents if match_cond.match(x)]

class FilesystemMatch:
    def __init__(self, fn, *args):
        self.fn = fn
        self.args = args

    def match(self, dir_content):
        return self.fn(dir_content, *self.args)

file_ends_with = partial(FilesystemMatch, fn=str.endswith)
file_ends_with_json = file_ends_with('json')

is_a_dir = partial(FilesystemMatch, fn=os.path.isdir)
