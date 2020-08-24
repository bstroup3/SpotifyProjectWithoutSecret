
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

SPOTIPY_CLIENT_ID = "821a2836760b4990b1bec51520a7bc43"
SPOTIPY_CLIENT_SECRET = "bcef5b3d0b9646a685b9b82c03399756"
REDIRECT_URI = "http://localhost:8888/callback"
user = "bds425"


client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = " user-read-recently-played playlist-modify-public user-follow-read user-read-email"
token = util.prompt_for_user_token(user, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)

else:
    print("Can't get token for" + user)

playlist_id = {}
temp = sp.user_playlists(user)
for x in temp['items']:
    name = x['name']
    id = x['id']
    playlist_id[name] = id

def view_owned_playlists():
    print("What playlist would you like to view?")
    request = input()

    playlist = sp.playlist(playlist_id[request])
    print("Playlist Name:")
    print(playlist["name"])
    print("Songs:")
    for x in playlist["tracks"]["items"]:
        track = x["track"]["name"]
        print(track)

def create_new_playlist():
    print("What would you like to name the playlist?")
    playlist_name = input()
    sp.user_playlist_create(user, playlist_name, True)

def view_followed_artists():
    followed_artists = sp.current_user_followed_artists()
    for x in followed_artists["artists"]["items"]:
        artists = x["name"]
        print(artists)

def add_items_to_playlist():
    print("which playlist would you like to add songs to?")
    playlist = input()

    Songs = sp.current_user_recently_played()
    song_id = {}
    for x in Songs["items"]:
        name = x["track"]["name"]
        id = x["track"]["id"]
        song_id[name] = id
        print(name)
    print("Which song/songs would you like to add?")
    add_song = input()
    idOFSong = song_id[add_song]
    randomList = []
    randomList += [idOFSong]
    sp.user_playlist_add_tracks(user, playlist_id[playlist], randomList)





while 1:

    temp = sp.user_playlists(user)
    for x in temp['items']:
        name = x['name']
        id = x['id']
        playlist_id[name] = id

    print("What would you like to do?")
    print("1. View owned playlists")
    print("2. View followed artists")
    print("3. Make a new playlist")
    print("4. Add songs to a playlist")
    print("99. Exit program")
    print("Pick a number:")
    Request = input()

    if Request == "1":
        view_owned_playlists()
    elif Request == "2":
        view_followed_artists()
    elif Request == "3":
        create_new_playlist()
        print("playlist created")
    elif Request == "4":
        add_items_to_playlist()
    else:
        print("That is not an option")
        print()
        continue

    print()
    print("Would you like to do something else?")
    again = input()
    if again == "yes":
        print()
        continue
    else:
        break
