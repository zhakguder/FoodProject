#!/usr/bin/env python3

import os
import requests
from sys import argv


# argv[1] is the path to image
path_img = argv[1]
url = "http://sbbi-panda.unl.edu:8888/predict-label/"
with open(path_img, "rb") as img:
    name_img = os.path.basename(path_img)
    files = {"image": (name_img, img, "multipart/form-data", {"Expires": "0"})}
    with requests.Session() as s:
        r = s.post(url, files=files)
        print(r.status_code)
        print(r.text)
