import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid = '8cbf98df7ac84b1a86633c4da3178f2f'
secret = '980a89d78db24fc8bc8e36cfe2c2abe7'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

