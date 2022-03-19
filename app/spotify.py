import spotipy
from app.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_SCOPE, SPOTIPY_OAUTH_CACHE, SPOTIPY_NUM_RECS

def connect_spotipy(): 
    auth_manager = spotipy.SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp
    
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
