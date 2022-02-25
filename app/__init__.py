from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import json
import sys
from app import spotify # requires from app, needed to init Flask with "app" isntead of __name__

def create_app(): 
    app = Flask('app')
    app.config.from_pyfile('config.py', silent = True)

    @app.route('/', methods = ['GET', 'POST'])
    def index(): 
        spotipy_object = spotify.connect_spotify()
        available_genres = spotify.get_available_genres(spotipy_object)
        playlist_recs = None 
        if request.method == 'POST':
            print('POST request received', file = sys.stdout)
            selectedGenres = request.get_json()['selectedGenres']    
            playlist_recs = spotify.get_recommendations(spotipy_object, selectedGenres, available_genres) # this returns a list of dictionaries where each dictionay corresponds to a recommended track
            response = make_response(render_template('recommendations.html', genres = available_genres, recommended_tracks = playlist_recs, test = "data type issue?"))      
            return response
        else: 
            return render_template('index.html', genres = available_genres)
            
    return app
