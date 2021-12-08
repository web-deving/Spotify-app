import pandas as pd
import numpy as np
from numpy.linalg import norm
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.cred import *
import tekore as tk
from datetime import date

#one artist for now maybe have user input artist? or Genre?

#asking for permission to analyze liked songs instead

#algorithm using the valence-arousal plane
def authorize_general():
    app_token = tk.request_client_token(cid, secret)
    return tk.Spotify(app_token)

def authorize_specific():
    scope = 'user-library-read user-top-read playlist-modify-public user-read-recently-played'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret= secret, redirect_uri= redirect_url, scope=scope))
    print("does it ask here?") #  yes
    return sp

#Recommendation Alg from https://towardsdatascience.com/build-your-first-mood-based-music-recommendation-system-in-python-26a427308d96

#  takes in valence and energy numbers, dataframe, api, and num of songs wanted 
def recommend_general(valence, energy, n_recs):
    #  read in dataframe
    target = os.path.join("app/",'valence_arousal_dataset.csv')
    ref_df = pd.read_csv(target)

    #  valence + energy = mood vector for each track
    ref_df["mood_vec"] = ref_df[["valence", "energy"]].values.tolist()
    #  authorize
    sp = authorize_general()
    track_moodvec = np.array([valence, energy])
    # Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    # Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)

    results = ref_df_sorted.iloc[:n_recs] #  can index the song info
    ids = results["id"].to_string(index=False, header = False)  #  split by "/n" if a list
    #print(ids.split("\n")[0])
    #print(results.to_string(index = False, header=False))
    #result = result.to_string(index = False, header = False)
    #recommend_specific(0.1,0.5,4)
    return ids


def make_playlist(ids):
    #sp = authorize_specific()
    scope = 'user-library-read user-top-read playlist-modify-public user-read-recently-played'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret= secret, redirect_uri= redirect_url, scope=scope))
    print("does it ask here?")
    user_data = sp.current_user()
    print("or here?")
    user_id = user_data["id"]
    today = date.today()
    playlist = sp.user_playlist_create(user_id, "Muzica ", today.strftime("%/b-%/d-%Y"))
    playlist_id = playlist["id"]
    songs = []
    for id in ids.split("\n"):
        songs.append(id)
    
    sp.user_playlist_add_tracks(user_id, playlist_id,songs)
    return playlist["id"]

#  takes in valence and energy numbers, rather than dataframe take in liked songs,
#  api, and num of songs wanted 

def recommend_specific(valence, energy, n_recs,):
    sp = authorize_specific()
    results = sp.current_user_recently_played()
    for idx, item in enumerate(results['items'][:3]):
        track = item['track']
        print(idx)
    # 2. Compute distances to all reference tracks
    # 3. Sort distances from lowest to highest
    #  do this but for all the tracks in array?
    # 4. If the input track is in the reference set, it will have a distance of 0, but should not be recommendended
    #  ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
    # 5. Return n recommendations
    #  return ref_df_sorted.iloc[:n_recs]
