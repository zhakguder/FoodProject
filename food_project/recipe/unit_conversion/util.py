#!/usr/bin/env python3

import json
from collections import defaultdict

def read_json(path):
    with open(path, 'rb') as f:
        content = json.load(f)
    return content

#needs_conversion = 'data/recipes/unit_conversion/corrected_meta.json'
needs_conversion = 'data/recipes/unit_conversion/cup_ingr.json'
to_convert_json = read_json(needs_conversion)

data = defaultdict(list)
for entry in to_convert_json['data']:
    data[entry[3]].append(entry[1])


tmp = {}
total = 0
total_uniq = 0
for k, v in data.items():
    total += len(v)
    try:
        tmp[k] = list(set(v))
        total_uniq += len(tmp[k])
    except:
        breakpoint()

with open('data/recipes/unit_conversion/cup_units_ingredients_no_repeat.json', 'w') as f:
    json.dump(tmp, f)
