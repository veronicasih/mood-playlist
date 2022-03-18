from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for, session
from flask_session import Session
import sys
from app import spotify # requires from app, needed to init Flask with "app" isntead of __name__
from app.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_SCOPE, SPOTIPY_OAUTH_CACHE, SPOTIPY_NUM_RECS
import os
import uuid
import spotipy

def create_app(): 
    app = Flask('app')

    ### trying smt out
    app.config.from_pyfile('config.py', silent = True)
    app.config['SECRET_KEY'] = os.urandom(64)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    Session(app)

    if not os.path.exists(SPOTIPY_OAUTH_CACHE):
        os.makedirs(SPOTIPY_OAUTH_CACHE)
    
    def session_cache_path():
        return SPOTIPY_OAUTH_CACHE + session.get('uuid')
    #########

    @app.route('/', methods = ['GET', 'POST'])
    def index(): 
        # spotipy_obj = spotify.connect_spotify()

        #### trying smt out
        if not session.get('uuid'):
            # Step 1. Visitor is unknown, give random ID
            session['uuid'] = str(uuid.uuid4())

        cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
        auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, 
                                                    client_secret=SPOTIPY_CLIENT_SECRET, 
                                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                                    scope=SPOTIPY_SCOPE,
                                                    cache_handler=cache_handler, 
                                                    show_dialog=True)
        print("HI")
        print(auth_manager)
        if request.args.get("code"):
            # Step 3. Being redirected from Spotify auth page
            print(auth_manager.get_access_token(as_dict=True))
            auth_manager.get_access_token(request.args.get("code"))
            return redirect('/')
        else:
            print(auth_manager.get_access_token(as_dict=True))


        if not auth_manager.validate_token(cache_handler.get_cached_token()):
            # Step 2. Display sign in link when no token
            auth_url = auth_manager.get_authorize_url()
            return f'<h2><a href="{auth_url}">Sign in</a></h2>'

        # Step 4. Signed in, display data
        spotipy_obj = spotipy.Spotify(auth_manager=auth_manager)
        print(spotipy_obj)
        #####

        available_genres = spotify.get_available_genres(spotipy_obj)
        if request.method == 'POST':
            print('POST request received', file = sys.stdout)
            selectedGenres = request.get_json()['selectedGenres']    
            playlist_recs = spotify.get_recommendations(spotipy_obj, selectedGenres, available_genres) # this returns a list of dictionaries where each dictionay corresponds to a recommended track
            return render_template('recommendations.html', genres = available_genres, themes = app.config['THEMES'], recommended_tracks = playlist_recs)
        else: 
            return render_template('index.html', genres = available_genres, themes = app.config['THEMES'])
            
    return app

