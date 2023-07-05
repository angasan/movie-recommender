"""
Constants, helper and utility functions used in this project.
"""
import pickle
import pandas as pd

RATINGS = pd.read_csv('data/user_item_matrix.csv', index_col=0)
MOVIES = RATINGS.columns.unique()
RATINGS_DF = pd.read_csv('data/ml-latest-small/ratings.csv')
MOVIES_DF = pd.read_csv('data/ml-latest-small/movies_mean_ranking.csv', index_col=0)

# Models to be used
with open('models/nmf_model.pkl', 'rb') as file:
    nmf_model = pickle.load(file)

with open('models/similarity_model.pkl', 'rb') as file:
    cos_sim_model = pickle.load(file)