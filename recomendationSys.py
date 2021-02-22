#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("netflix_titles.csv")

mov = df.query("type == 'Movie'")
movies = mov[["title", "director", "cast", "country", "rating", "listed_in"]].reset_index()
movies["title"] = movies["title"].apply(lambda x : x.lower())
 
def binariza(col, classe):
    classe[col] = classe[col].fillna("Not Informed")
    
    lista = []
    for i in classe[col]:
        lista_aux = i.split(",")
        for j in lista_aux:
            lista.append(j)

    lista_sort = sorted(set(lista))

    binary_lista = [[0] * 0 for i in range(len(set(lista)))]

    for i in classe[col]:
        c = 0
        for j in lista_sort:
            if j in i:
                binary_lista[c].append(1.0)
            else:
                binary_lista[c].append(0.0)
            c+=1

    return pd.DataFrame(binary_lista).T


bin_actors = binariza("cast", movies)
bin_director = binariza("director", movies)
bin_country = binariza("country", movies)
bin_rating = binariza("rating", movies)
bin_listed_in = binariza("listed_in", movies)
bin_df = pd.concat([bin_actors, bin_director, bin_country, bin_rating, bin_listed_in], axis=1, ignore_index=True)
cs_df = pd.DataFrame(cosine_similarity(bin_df))

cs_df.to_csv("cs_df.csv")

