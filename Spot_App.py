
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

def view_owned_playlists():
    print("What playlist would you like to view?")
    request = input()

    playlist_id = {}

    temp = sp.user_playlists(user)
    for x in temp['items']:
        name = x['name']
        id = x['id']
        playlist_id[name] = id
    playlist = sp.playlist(playlist_id[request])
    print("Playlist Name:")
    print(playlist["name"])
    print("Songs:")
    for x in playlist["tracks"]["items"]:
        track = x["track"]["name"]
        print(track)
def create_new_playlist(): #FIX ME
    print("What would you like to name the playlist?")
    playlist_name = input()
    sp.user_playlist_create(user, playlist_name)

print("What would you like to do?")
print("1. View owned playlists")
print("2. Make a new playlist")
print("Pick a number:")
Request = input()

if Request == "1":
    view_owned_playlists()
if Request == "2":
    create_new_playlist()




