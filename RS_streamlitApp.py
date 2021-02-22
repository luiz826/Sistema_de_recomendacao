#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

cs_df = pd.read_csv("cs_df.csv")
df = pd.read_csv("netflix_titles.csv")

mov = df.query("type == 'Movie'")
movies = mov[["title", "director", "cast", "country", "rating", "listed_in"]].reset_index()
movies["title"] = movies["title"].apply(lambda x : x.lower())
movies = movies.drop(["index"], axis=1)

def recomendation(movie):
    
    movie = movie.lower()
    
    if movie in movies["title"].values:
        idm = movies.loc[movies["title"] == movie].index.item()
        rm = cs_df[str(idm)].sort_values(ascending=False).head(6)[1:]
        print(rm)
        movies_c = movies.copy()
        movies_c["CS"] = cs_df[str(idm)].sort_values(ascending=False)

        return movies_c.iloc[rm.index][["title", "director"]]
    
    st.write("Esse filme não está na nossa base de dados...\n")
    st.write("ou você quis dizer: ", end="")
    for i in movies["title"].values:
        if movie in i:
            st.write(i)

                   
st.title("Sistema de recomendação de filmes da Netflix")

st.image("https://i.pinimg.com/originals/da/f3/0f/daf30fac5e16393d66a3684dd27e29af.png")

st.write("Já ficou em dúvida de qual filme assistir? rolou o catálogo da Netflix até cansar?\nSeus problemas acabaram! basta digitar o nome do filme que você gosta e nós recomendaremos 5 filmes para você!")

option = st.text_input("Digite o nome do filme (em inglês):", "Pulp Fiction")

st.dataframe(recomendation(option), width=1000, height=400)
