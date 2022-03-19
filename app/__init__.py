import sys
from flask import Flask, request, render_template
from app import spotify 

def create_app():
    app = Flask('app')
    app.config.from_pyfile('config.py', silent = True)

    @app.route('/', methods = ['GET', 'POST'])
    def index():
        spotipy_obj = spotify.connect_spotipy()
        available_genres = spotify.get_available_genres(spotipy_obj)
        if request.method == 'POST':
            print('POST request received', file = sys.stdout)
            selectedGenres = request.get_json()['selectedGenres']    
            playlist_recs = spotify.get_recommendations(spotipy_obj, selectedGenres, available_genres) # this returns a list of dictionaries where each dictionay corresponds to a recommended track
            return render_template('recommendations.html', genres = available_genres, themes = app.config['THEMES'], recommended_tracks = playlist_recs)
        else: 
            return render_template('index.html', genres = available_genres, themes = app.config['THEMES'])

    return app