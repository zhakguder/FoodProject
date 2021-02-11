#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from food_project.recipe import (
    connect_to_database,
    get_processed_ingredients_from_db,
    save_cluster_df,
)
from food_project.recipe.similarity import entropy_update


load_dotenv()
uri = os.getenv("MONGODB_URI")
uname = os.getenv("MONGODB_USERNAME")
pwd = os.getenv("MONGODB_PWD")

connect_to_database(uri, uname, pwd)

res = get_processed_ingredients_from_db()
entropy_update(res)

save_cluster_df("data/recipes/cluster_ingredients.df")
