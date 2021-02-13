#!/usr/bin/env python3

from food_project.image_classification.crf.crf_model import CRF
from food_project.image_classification.crf.prediction_class_clusters import \
    ClassCandidates
from food_project.image_classification.crf.preprocess import (
    get_individual_image, read_image, split_image)

# crf = CRF(5, 10)

# node1 = ClassCandidates({"apple": 0.5, "orange": 0.3, "cheese": 0.1})
# node2 = ClassCandidates({"cheese": 0.1, "lemon": 0.3, "bread": 0.4, "pepper": 0.1})
# crf.add_node(node1)
# crf.add_node(node2)
# crf.make_full()
# res, best = crf.get_best_config()

# 3x3 image grid
v_n = 3
h_n = 3
image = read_image("data/crf/test_images/compiled/1.jpeg")
splitted_image = split_image(image, v_n, h_n)
res = get_individual_image(splitted_image, 0, 1)


from PIL import Image

img = Image.fromarray(res)
img.show()
