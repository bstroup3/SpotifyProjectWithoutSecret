import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

Cid = "821a2836760b4990b1bec51520a7bc43"
Secret = "bcef5b3d0b9646a685b9b82c03399756"
user = ""

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-library-read playlist-read-private'
token = 'util.promt_for_user_token(username,scope)'

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for" + username)
