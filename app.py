# https://code.visualstudio.com/docs/python/tutorial-flask
# follow this to create virtual environment for flask

from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth


app = Flask(__name__) 

# sign the session or a cookie
app.secret_key = "random_gen"
app.config['SESSION_COOKIE_NAME'] = 'spotify_api_cookie'

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url) 

@app.route('/redirect')
def redirectPage():
    return 'redirect'

@app.route('/getTracks')
def getTracks():
    return 'Some songs'

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='cac90d6e6fbe4d1a899738792481b071',
        client_secret="82544bf92fce46f6bc3a1f0f4a09eb64",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read")
