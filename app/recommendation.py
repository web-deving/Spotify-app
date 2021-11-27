from numpy.linalg.linalg import _determine_error_states
import pandas as pd
import random

from pandas.core import api
import authorization
import numpy as np
from numpy.linalg import norm

#read in dataframe
df_general = pd.read_csv("valence_arousal_dataset.csv")
df_specific = authorization.authorize_specific()
#valence + energy = mood vector
df_general["mood_vec"] = df_general[["valence", "energy"]].values.toList()
df_specific["mood_vec"] = df_specific[["valence", "energy"]].values.toList()

#authorize
sp = authorization.authorize_general()

#Recommendation Alg from https://towardsdatascience.com/build-your-first-mood-based-music-recommendation-system-in-python-26a427308d96

#  takes in valence and energy numbers, dataframe, api, and num of songs wanted 
def recommend_general(valence, energy, ref_df = df_general, sp, n_recs):
    
    # 1. Crawl valence and arousal of given track from spotify api
    track_features = sp.track_audio_features(track_id)
    track_moodvec = np.array([track_features.valence, track_features.energy])
    
    # 2. Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    # 3. Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    # 4. If the input track is in the reference set, it will have a distance of 0, but should not be recommendended
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
    # 5. Return n recommendations
    return ref_df_sorted.iloc[:n_recs]

#  takes in valence and energy numbers, rather than dataframe take in liked songs,
#  api, and num of songs wanted 
def recommend_specific(valence, energy, ref_df = df_specific, sp, n_recs):
    # 1. Crawl valence and arousal of given track from spotify api
    track_features = sp.track_audio_features(track_id)
    track_moodvec = np.array([track_features.valence, track_features.energy])
    
    # 2. Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    # 3. Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    # 4. If the input track is in the reference set, it will have a distance of 0, but should not be recommendended
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
    # 5. Return n recommendations
    return ref_df_sorted.iloc[:n_recs]