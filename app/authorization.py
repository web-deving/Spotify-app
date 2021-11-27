import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred 
import tekore as tk
#one artist for now maybe have user input artist? or Genre?

#asking for permission to analyze liked songs instead

#algorithm using the valence-arousal plane
def authorize_general():
    app_token = tk.request_client_token(cred.cid, cred.secret)
    return tk.Spotify(app_token)
def authorize_specific():
    scope = 'user-library-read user-top-read playlist-modify-public user-read-recently-played'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.cid, client_secret= cred.secret, redirect_uri=cred.redirect_url, scope=scope))

    results = sp.current_user_recently_played()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])




