from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
import json
import sys
from app import spotify # requires from app, needed to init Flask with "app" isntead of __name__

def create_app(): 
    app = Flask('app')
    app.config.from_pyfile('config.py', silent = True)

    @app.route('/', methods = ['GET', 'POST'])
    def index(): 
        print(spotify.hello_world(), file = sys.stdout)
        spotipy_object = spotify.connect_spotify()

        available_genres = spotify.get_available_genres(spotipy_object)
        print(available_genres, file = sys.stdout)
        print(type(available_genres))
        
        playlist_recs = None 
        if request.method == 'POST':
            print('POST request received', file = sys.stdout)
            selectedGenres = request.get_json()['selectedGenres']        
            playlist_recs = spotify.get_recommendations(spotipy_object, selectedGenres, available_genres) # this returns a list of dictionaries where each dictionay corresponds to a recommended track
            # print(updated_playlist, file = sys.stdout)
            message = playlist_recs
            print(playlist_recs)
            response = make_response(render_template('recommendations.html', genres = available_genres, recommended_tracks = playlist_recs, test = "data type issue?"))      
            response.headers['result'] = message
            return response
        else: 
            return render_template('index.html', genres = available_genres)
            
    return app

# def clean_up_response(playlist_recs):
#     updated_playlist = []
#     for track in playlist_recs: 
#             artists = get_artists(track['artists'])
#             track = {'name' : track['name'], 'artists': artists, 'cover_art' : track['album']['images'][0], 'spotify_url' : track['external_urls']['spotify'], 'sample' : track['linked_from']['preview_url']}
#             updated_playlist.append(track)
#     return updated_playlist 

# # artists is an array of artists
# def get_artists(artists_arr): 
#     artists = [artist['name'] for artist in artists_arr]
#     return artists 
# <!-- onclick="playAudio({{loop.index}})" 
