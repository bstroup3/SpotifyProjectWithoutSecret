import export as export
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

SPOTIPY_CLIENT_ID = '821a2836760b4990b1bec51520a7bc43'
SPOTIPY_CLIENT_SECRET = 'bcef5b3d0b9646a685b9b82c03399756'
user = "bds425"

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-library-read playlist-read-private'
token = util.prompt_for_user_token(user, scope)

if token:
    sp = spotipy.Spotify(auth=token)

else:
    print("Can't get token for" + user)
