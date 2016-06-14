# -*- coding: utf-8 -*-
import json


def read_data():
    fin = open("data/1099641070.txt")
    posts = []

    try:
        while True:
            line = fin.readline()
            obj = json.loads(line)
            posts.append(obj)
            if len(posts) > 5000:
                break
    finally:
        fin.close()

    return posts

