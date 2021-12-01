import pandas as pd
from app.authorization import *
import numpy as np
from numpy.linalg import norm
import os
#Recommendation Alg from https://towardsdatascience.com/build-your-first-mood-based-music-recommendation-system-in-python-26a427308d96

#  takes in valence and energy numbers, dataframe, api, and num of songs wanted 
def recommend_general(valence, energy, n_recs):
    #  read in dataframe
    target = os.path.join("app/",'valence_arousal_dataset.csv')
    ref_df = pd.read_csv(target)
    # df_specific = authorization.authorize_specific()
    #  valence + energy = mood vector for each track
    
    ref_df["mood_vec"] = ref_df[["valence", "energy"]].values.tolist()
    # df_specific["mood_vec"] = df_specific[["valence", "energy"]].values.toList()
    #  authorize
    sp = authorize_general()
    track_moodvec = np.array([valence, energy])
    # 2. Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    # 3. Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    # 4. Return n recommendations

    result = ref_df_sorted.iloc[:n_recs] #  can index the song info
    result = result.to_string(index = False, header = False)
    return result

#  takes in valence and energy numbers, rather than dataframe take in liked songs,
#  api, and num of songs wanted 
def recommend_specific(valence, energy, sp, n_recs,):
    track_moodvec = np.array([valence, energy])
    # 2. Compute distances to all reference tracks
    # 3. Sort distances from lowest to highest
    #  do this but for all the tracks in array?
    # 4. If the input track is in the reference set, it will have a distance of 0, but should not be recommendended
    #  ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
    # 5. Return n recommendations
    #  return ref_df_sorted.iloc[:n_recs]