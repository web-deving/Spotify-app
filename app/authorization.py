import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.cred import *
import tekore as tk
#one artist for now maybe have user input artist? or Genre?

#asking for permission to analyze liked songs instead

#algorithm using the valence-arousal plane
def authorize_general():
    app_token = tk.request_client_token(cid, secret)
    return tk.Spotify(app_token)

def authorize_specific():
    scope = 'user-library-read user-top-read playlist-modify-public user-read-recently-played'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.cid, client_secret= cred.secret, redirect_uri=cred.redirect_url, scope=scope))

    results = sp.current_user_recently_played()  # change to whole library of liked songs
    #  write algo to store all liked songs in dataset like in dataset 
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])




