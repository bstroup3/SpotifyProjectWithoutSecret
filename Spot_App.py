
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import tkinter as tk

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


def view_owned_playlists(request):

    try:
        playlist = sp.playlist(playlist_id[request])
        print("Playlist Name:")
        print(playlist["name"])
        print("Songs:")
        for x in playlist["tracks"]["items"]:
            track = x["track"]["name"]
            print(track)
    except:
        popUp = tk.Tk()
        popUp.config(bg="#191414")
        popUp.geometry("200x50")
        popUp.title('Error')
        message = tk.Label(popUp, text="Playlist not found\n Try again", foreground="red", bg="#191414", font="Arial 20")
        message.pack()


def create_new_playlist():
    print("What would you like to name the playlist?")
    playlist_name = input()
    sp.user_playlist_create(user, playlist_name, True)
    print("playlist created")

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
    idOfSong = song_id[add_song]
    randomList = []
    randomList += [idOfSong]
    sp.user_playlist_add_tracks(user, playlist_id[playlist], randomList)
    print("song/songs added")

def remove_songs_from_playlist():
    print("which playlist would you like to remove songs from?")
    request = input()

    try:
        playlist = sp.playlist(playlist_id[request])
        print("Playlist Name:")
        print(playlist["name"])
        print("Songs:")
        song_id = {}
        for x in playlist["tracks"]["items"]:
            track = x["track"]["name"]
            id = x["track"]["id"]
            song_id[track] = id
            print(track)

        removed_songs = []

        while 1:
            print("Which song would you like to remove?")
            song = input()
            idOfSong = song_id[song]
            removed_songs += [idOfSong]
            print("would you like to remove another song?")
            answer = input()
            if answer == "yes" or answer == "Yes":
                continue
            else:
                break
        sp.user_playlist_remove_all_occurrences_of_tracks(user, playlist_id[request], removed_songs)
        print("song/songs removed")

    finally:
        print("Could not find Playlist")
        return


def add_image_to_playlist():
    print("What playlist?")
    request = input()
    print("Go to this website to convert and copy Base64 data: https://onlinejpgtools.com/convert-jpg-to-base64")
    print("Paste data image")
    requestImage = input()
    addInto = playlist_id[request]
    sp.playlist_upload_cover_image(playlist_id=addInto, image_b64=requestImage)
    print("Image added")



while 1:
    temp = sp.user_playlists(user)
    for x in temp['items']:
        name = x['name']
        id = x['id']
        playlist_id[name] = id

    window = tk.Tk()
    window.title('Spotify App')
    window.config(bg="#191414")
    window.geometry("400x300")
    global greeting
    greeting = tk.Label(window, text="Spotify App\nCreated by Ben Stroup", foreground="#1DB954", background="#191414", padx=100, pady=10)
    greeting.grid(row=1, column=1)

    def update_to_main():
        greeting.config(text="What would you like to do?")
        startButton.config(text="View Followed Artists", command=view_followed_artists)
        viewPlaylist = tk.Button(window, text="View Owned Playlists", command=viewOwnedPlaylist, activeforeground="#1DB954", highlightbackground="#191414")
        viewPlaylist.grid(row=3, column=1)
        createPlaylist = tk.Button(window, text="Create Playlist", command=create_new_playlist, activeforeground="#1DB954", highlightbackground="#191414")
        createPlaylist.grid(row=4, column=1)
        addItemPlaylist = tk.Button(window, text="Add Items To Playlist", command=add_items_to_playlist, activeforeground="#1DB954", highlightbackground="#191414")
        addItemPlaylist.grid(row=5, column=1)
        removeSongPlaylist = tk.Button(window, text="Remove Items on Playlist", command=remove_songs_from_playlist, activeforeground="#1DB954", highlightbackground="#191414")
        removeSongPlaylist.grid(row=6, column=1)
        addImagePlaylist = tk.Button(window, text="Add Image to a Playlist", command=add_image_to_playlist, activeforeground="#1DB954", highlightbackground="#191414")
        addImagePlaylist.grid(row=7, column=1)

    global viewOwnedPlaylist

    def viewOwnedPlaylist():
        newWindow = tk.Tk()
        newWindow.title('Spotify App')
        newWindow.config(bg="#191414")
        newWindow.geometry("400x400")
        Label = tk.Label(newWindow, text="Which playlist would you like to view?", fg="#1DB954", background="#191414")
        Label.pack()

        global entry
        entry = tk.Entry(newWindow, bg="#696969")
        entry.pack()

        playlistDisplay = tk.Button(newWindow, text="Enter", command=playlist_display, activeforeground="#1DB954", highlightbackground="#191414")
        playlistDisplay.pack()


    def playlist_display():
        name_var = entry.get()
        print(name_var + "test")
        view_owned_playlists(name_var)


    global startButton
    startButton = tk.Button(window, text="Start", command=update_to_main, activeforeground="#1DB954", highlightbackground="#191414")
    startButton.grid(row=2, column=1)

    window.mainloop()



    if Request == "1":
        view_owned_playlists()
    elif Request == "2":
        view_followed_artists()
    elif Request == "3":
        create_new_playlist()
    elif Request == "4":
        add_items_to_playlist()
    elif Request == "5":
        remove_songs_from_playlist()
    elif Request == "6":
        add_image_to_playlist()
    else:
        print("That is not an option")
        print()

    print()
    print("Would you like to do something else?")
    again = input()
    if again == "yes":
        print()
        continue
    else:
        break
