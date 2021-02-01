#!/usr/bin/env python3

import pickle
import pandas as pd
import json
import os
import re
from functools import partial
from difflib import SequenceMatcher


def read_json(path):
    with open(path, "r") as f:
        content = json.load(f)
    return content


def read_pickle(path, encoding=None):
    with open(path, "rb") as f:
        if encoding:
            content = pickle.load(f, encoding=encoding)
        else:
            content = pickle.load(f)
    return content


def column_name(df, i):
    return df.columns[i]


def column_value(df, i):
    return df.iloc[:, i]


def dataframe_from_dict(mydict):
    return pd.DataFrame(mydict)

def dataframe_from_list(lst, columns):
    return pd.DataFrame(lst, columns=columns)

def save_dataframe(df, path):
    try:
        df.to_pickle(path)
    except:
        raise Exception("Couldn't save dataframe!")


def series_from_dict(mydict):
    return pd.Series(mydict)


def matching_columns(df, text):
    return df.columns.str.contains(text)


def _content_matches(path, match_cond):
    return match_cond.match(path)


def list_content_with_matches(path, match_cond):
    contents = os.listdir(path)

    def abs_path(x):
        return os.path.join(path, x)

    return [abs_path(x) for x in contents if match_cond.match(abs_path(x))]


def clean_word(inp, word, sep="_"):
    """Removes word from inp and returns modified inp"""
    inp = _change_plus(inp)
    if word in inp:
        words = inp.split(sep)
        words = [x for x in words if x != word]
        return sep.join(words)
    else:
        return inp


def _change_plus(word, sep="_", unwanted_sep="+"):
    words = word.split(unwanted_sep)
    return sep.join(words)


class FilesystemMatch:
    def __init__(self, fn, *args):
        self.fn = fn
        self.args = args

    def match(self, dir_content):
        return self.fn(dir_content, *self.args)


def comparison(fn, *args):
    return FilesystemMatch(fn, *args)


def match_score(text, query):

    match = re.search(query, text)

    if not match:
        return 0

    start, end = match.span()
    return (end - start) / len(text)


def uniform_score(text, query):

    return 1


def matchsubstring(m, n, verbose=0):
    seqMatch = SequenceMatcher(None, m, n)
    match = seqMatch.find_longest_match(0, len(m), 0, len(n))
    if verbose and match.size:
        print("Common Substring ::>", m[match.a : match.a + match.size])
    return match.size
