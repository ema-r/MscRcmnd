import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid = '458c511cb460490c87984d079bc5a290'
secret = '7ca35c86a8da4b688e14aa9514405b3b'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

