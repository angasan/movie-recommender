"""
File where the different pages of the app are modelled
"""

import streamlit as st
from IPython.display import HTML
import json

from recommenders import (
    nmf_recommendations,
    cos_sim_recommendations,
    random_recommendations
    )

from utils import MOVIES

def home():

    # slogan
    st.write(
        """*Movies are like magic tricks (Jeff Bridges)*"""
        )
    
    # Write a description explaining the user what the app does
    st.write(
        """
        ### Not sure what to watch? Then you came to the right place! 

        This is a **movie recommender**. 
        
        Here you won't have to decide anymore between millions and millions of movies,
        just choose the type of recommendation for you and we'll give you the answer 
        you have been looking for.
        """
        )

    # blank space
    st.write("")

    # title
    st.title("Rate Movies")
    #
    col1, _, col3 = st.columns([10,1,5])

    with col1:
        m1 = st.selectbox("movie 1", MOVIES)
        st.write("")
        m2 = st.selectbox("movie 2", MOVIES)
        st.write("")
        m3 = st.selectbox("movie 3", MOVIES)
        st.write("")
        m4 = st.selectbox("movie 4", MOVIES)
        st.write("")
        m5 = st.selectbox("movie 5", MOVIES) 
    
    with col3:
        r1 = st.slider(
            label="rating 1",
            min_value=1,
            max_value=5,
            value=3
            ) 
        r2 = st.slider(
            label="rating 2",
            min_value=1,
            max_value=5,
            value=3
            ) 
        r3 = st.slider(
            label="rating 3",
            min_value=1,
            max_value=5,
            value=3
            ) 
        r4 = st.slider(
            label="rating 4",
            min_value=1,
            max_value=5,
            value=3
            ) 
        r5 = st.slider(
            label="rating 5",
            min_value=1,
            max_value=5,
            value=3
            ) 

    query_movies = [m1,m2,m3,m4,m5]
    query_ratings = [r1,r2,r3,r4,r5]
    
    user_query = dict(zip(query_movies,query_ratings))

    # get user query
    st.markdown("###")

    if st.button(label="save user query") :
        json.dump(
            user_query,
            open("data/user_query.json",'w')
            )

    # Possibly insert movie posters here (kind of netflix like maybe?)

def similarity_recommender():
    # title
    st.title("Movie Recommendations")

    user_query = json.load(open("data/user_query.json"))
    recommendations = cos_sim_recommendations(user_query, 10)
    
    st.write("")
    st.write("This are the top 10 movies for you:")
    st.write(recommendations)


def rating_recommender():
    # title
    st.title("Movie Recommendations")

    user_query = json.load(open("data/user_query.json"))
    recommendations = nmf_recommendations(user_query, 10)

    st.write("")
    st.write("This are the top 10 movies for you:")
    st.write(recommendations)

def random_recommender():

    # title
    st.title("Popular Movies")
    col1, _, col3, col4 = st.columns([10,1,5,5])

    with col1:
        n = st.slider(
        label="how many movies?",
        min_value=1,
        max_value=10
        ) 
    with col3:
        st.markdown("####")
        genre = st.checkbox("include genres")

    with col4:
        st.markdown("###")
        show_button = st.button(label="show movies") 
    
    recommendations_df = random_recommendations(int(n), genre)

    st.markdown("###")
    if show_button:
        st.write(
            HTML(recommendations_df.to_html(escape=False))
            )

