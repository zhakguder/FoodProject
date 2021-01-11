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

def _content_matches(path, match_cond):
    return match_cond.match(path)

def list_content_with_matches(path, match_cond):
    contents = os.listdir(path)
    def abs_path(x):
        return os.path.join(path, x)
    return  [abs_path(x) for x in contents if match_cond.match(abs_path(x))]

class FilesystemMatch:
    def __init__(self, fn, *args):
        self.fn = fn
        self.args = args

    def match(self, dir_content):
        return self.fn(dir_content, *self.args)

def comparison(fn, *args):
    return FilesystemMatch(fn, args)
# is_json = FilesystemMatch(str.endswith, 'json')
# is_dir = FilesystemMatch(os.path.isdir)
# is_jpg = FilesystemMatch(str.endswith, 'jpg')
# is_out = FilesystemMatch(str.endswith, 'out')
