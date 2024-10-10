# https://code.visualstudio.com/docs/python/tutorial-flask
# follow this to create virtual environment (venv) for flask

from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import time


app = Flask(__name__) 

# sign the session or a cookie
app.secret_key = "random_key"
app.config['SESSION_COOKIE_NAME'] = 'spotify_api_cookie'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url) 

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code') 
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in") 
        return redirect(url_for('login', _external=True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    # return sp.current_user_recently_played(limit=20)

    all_songs = [] 
    iter = 1
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=0)['items']
        iter += 1
        all_songs += items
        if (len(items) < 50):
            break
    return str(len(all_songs))

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth() 
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='cac90d6e6fbe4d1a899738792481b071',
        client_secret="82544bf92fce46f6bc3a1f0f4a09eb64",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read")
