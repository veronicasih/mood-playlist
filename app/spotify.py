import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_SCOPE, SPOTIPY_OAUTH_CACHE, SPOTIPY_NUM_RECS

def connect_spotify():
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE, cache_path = SPOTIPY_OAUTH_CACHE))
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE, cache_path = SPOTIPY_OAUTH_CACHE)
    print(sp_oauth.get_access_token(as_dict=True))
    return get_token(sp_oauth)

def get_token(sp):
    # used https://stackoverflow.com/questions/25711711/spotipy-authorization-code-flow 
    access_token = sp.get_access_token()
    # access_token = token.get('access_token')

    if access_token:
        print("Access token available!")
        sp_obj = spotipy.Spotify(access_token)
        return sp_obj
    else:
        return None

def get_available_genres(sp):
    return sp.recommendation_genre_seeds()['genres']

# Up to 5 seed values may be provided in any combination of seed_artists, seed_tracks and seed_genres.
def get_recommendations(sp, selected_genres, available_genres): 
    # if more than 5 genres are selected, default to first 5
    if (len(selected_genres) > 5): 
        selected_genres = selected_genres[0:4]
    # if no genres are selected, default to first available genre -> should there be a message that pops up?
    if (len(selected_genres) == 0): 
        selected_genres = [available_genres[0]]
    
    recommendations = sp.recommendations(seed_genres = selected_genres, limit = SPOTIPY_NUM_RECS)['tracks']
    updated_recommendations = clean_up_recommendations(recommendations)
    return updated_recommendations

def clean_up_recommendations(recommendations):
    updated_recs = []
    for track in recommendations: 
        artists = get_artists(track['artists'])
        track = {'name' : track['name'], 'artists': artists, 'cover_art' : track['album']['images'][0], 'spotify_url' : track['external_urls']['spotify'], 'sample' : track['preview_url']}
        updated_recs.append(track)
    return updated_recs 

# artists is an array of artists
def get_artists(artists_arr): 
    artists = [artist['name'] for artist in artists_arr]
    artists_str = ', '.join(artists)
    return artists_str

def hello_world():
    return "hello world. spotipy.py has been successfully imported."
