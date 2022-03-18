from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import sys
from app import spotify # requires from app, needed to init Flask with "app" isntead of __name__

def create_app(): 
    app = Flask('app')
    app.config.from_pyfile('config.py', silent = True)

    @app.route('/', methods = ['GET', 'POST'])
    def index(): 
        spotipy_object = spotify.connect_spotify()
        spotipy_token = spotify.get_token(spotipy_object)
        available_genres = spotify.get_available_genres(spotipy_object)
        if request.method == 'POST':
            print('POST request received', file = sys.stdout)
            selectedGenres = request.get_json()['selectedGenres']    
            playlist_recs = spotify.get_recommendations(spotipy_object, selectedGenres, available_genres) # this returns a list of dictionaries where each dictionay corresponds to a recommended track
            return render_template('recommendations.html', genres = available_genres, themes = app.config['THEMES'], recommended_tracks = playlist_recs)
        else: 
            return render_template('index.html', genres = available_genres, themes = app.config['THEMES'])
            
    return app
