
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

SPOTIPY_CLIENT_ID = "821a2836760b4990b1bec51520a7bc43"
SPOTIPY_CLIENT_SECRET = "bcef5b3d0b9646a685b9b82c03399756"
REDIRECT_URI = "http://localhost:8888/callback"
user = "bds425"


client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = "user-read-email"
token = util.prompt_for_user_token(user, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)

else:
    print("Can't get token for" + user)


print("What playlist would you like to view?")
request = input()

Playlist_id = {}

temp = sp.user_playlists(user)
for x in temp['items']:
    name = x['name']
    id = x['id']
    Playlist_id[name] = id
Playlist = sp.playlist(Playlist_id[request])
print("Playlist Name:")
print(Playlist["name"])
print("Songs:")
for x in Playlist["tracks"]["items"]:
    Track = x["track"]["name"]
    print(Track)







