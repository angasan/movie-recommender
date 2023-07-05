"""
File modeling the different recommenders that can be used in the app
"""
import random
import pandas as pd
import numpy as np
import streamlit as st

from scipy.sparse import csr_matrix

from utils import (
    nmf_model,
    cos_sim_model,
    MOVIES_DF, 
    RATINGS_DF,
    MOVIES
    )

def nmf_recommendations(user_query, k):
    """
    Movie recommendations based on NMF model

    Uses the NMF model saved from previous project to make movie recommendations 
    based on a new user query. In this new user query the user must rank some movies
    to create recommendations on.

    Args:
        user_query (dict): Dictionary of movies and their corresponding value
        k (int): Number of recommendations to be generated
    
    Returns:
        list: K recommendations based on NMF model
    """

    user_dataframe = pd.DataFrame(user_query, columns=MOVIES, index=["new_user"])
    user_dataframe = user_dataframe.fillna(0)

    Q = pd.DataFrame(
                nmf_model.components_,
                columns=MOVIES,
                index=nmf_model.get_feature_names_out()
            )

    P_new_user = pd.DataFrame(
            nmf_model.transform(user_dataframe),
            columns = nmf_model.get_feature_names_out(),
            index = ['new_user']
            )

    R_hat_new_user = pd.DataFrame(
            data=np.dot(P_new_user,Q),
            columns=MOVIES,
            index = ['new_user'])

    R_hat_new_user = R_hat_new_user.drop(user_query.keys(),axis=1)
    ranked = R_hat_new_user.T.sort_values(by=["new_user"],
                                          ascending=False
                                          ).index.tolist()
    
    return  pd.DataFrame(ranked[:k], columns=['Movies'])

def cos_sim_recommendations(user_query, k):
    """
    Movie recommendations based on Nearest Neighbours model

    Uses the KNN model saved from previous project to make movie recommendations 
    based on a new user query. 

    Args:
        user_query (dict): Dictionary of movies and their corresponding value
        k (int): Number of recommendations to be generated
    
    Returns:
        list: K recommendations based on KNN model
    """
        
    # Convert the user query to data the format needed
    user_dataframe = pd.DataFrame(
        user_query,
        columns=MOVIES,
        index=["new_user"]
        ).fillna(0)
    
    # Compute the similarity scores and neighbor ids for the movies using the
    # pre-trained model
    similarity_scores, neighbor_ids = cos_sim_model.kneighbors(
        user_dataframe,
        n_neighbors=5,
        return_distance=True
        )
    
    # Save ids and scores in a DataFrame and sort it
    df_neighbors = pd.DataFrame(
        data={
            "neighbor_id": neighbor_ids[0],
            "neighbor_title": user_dataframe.columns[neighbor_ids[0]],
            "similarity_score": similarity_scores[0],
        }
    )

    df_neighbors.sort_values("similarity_score", ascending=False, inplace=True)

    # Calculate CSR Matrix (R) and convert do Dataframe
    df_r = pd.read_csv('data/user_item_matrix.csv', index_col=0)

    # Filter to only show similar users and filter out movies rated by the user
    neighborhood_filtered = df_r.iloc[neighbor_ids[0]].drop(user_query.keys(), axis=1)

    # Multiply the ratings with the similarity score of each user and
    # calculate the summed up rating for each movie
    df_score = neighborhood_filtered.apply(
        lambda x: df_neighbors.set_index("neighbor_id").loc[x.index][
            "similarity_score"
        ]
        * x
    )
    df_score_ranked = (
        df_score.sum(axis=0).reset_index().sort_values(0, ascending=False)
    )
    df_score_ranked.reset_index(drop=True, inplace=True)

    return df_score_ranked.iloc[:k, 0]


def random_recommendations(k, genre=False):
    """
    Creates random recommendations of movies based on a weight.

    Uses the mean rating of the movie as a weight to make random choices
    for the list of movies in the df. 

    Args:
        k (int): Number of recommendations to be generated
    
    Returns:
        list: Random recommendations based on the weight
    """

    recommendations = random.choices(
            MOVIES_DF['title'],
            weights=MOVIES_DF['mean_rating'],
            k=k
        )
    
    genres = [
            MOVIES_DF[MOVIES_DF.title == movie]['genres'].iloc[0]
            for movie
            in recommendations
            ]
    
    if genre:
        return pd.DataFrame({'Movies': recommendations, 'Genres': genres})
    
    return pd.DataFrame(list(recommendations), columns=['Movies'])
