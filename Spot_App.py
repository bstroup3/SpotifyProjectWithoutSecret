
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import webbrowser
from tkinter import *


SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8888/callback"

global user
user = "bds425"


client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = "user-read-recently-played playlist-modify-public user-follow-read user-read-email user-read-private ugc-image-upload"
token = util.prompt_for_user_token(user, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)

else:
    print("Can't get token for" + user)

playlist_id = {}
global temp
temp = sp.user_playlists(user)
for x in temp['items']:
    name = x['name']
    id = x['id']
    playlist_id[name] = id


def view_owned_playlists(request):

    try:
        playlist = sp.playlist(playlist_id[request])
        songsList = Tk()
        songsList.title(playlist["name"])
        songsList.config(bg="#191414")
        songsList.geometry('300x300')

        tracks = ""

        for x in playlist["tracks"]["items"]:
            track = x["track"]["name"]
            tracks += track
            tracks += "\n"

        listOfSongs = Label(songsList, text="Songs\n" + tracks, fg="#1DB954", background="#191414")
        listOfSongs.pack()
    except:
        popUp = Tk()
        popUp.config(bg="#191414")
        popUp.geometry("200x50")
        popUp.title('Error')
        message = Label(popUp, text="Playlist not found\n Try again", foreground="red", bg="#191414", font="Arial 20")
        message.pack()


def create_new_playlist():
    createPlaylistWindow = Tk()
    createPlaylistWindow.geometry("400x400")
    createPlaylistWindow.title('Create New Playlist')
    createPlaylistWindow.config(bg="#191414")

    createLabel = Label(createPlaylistWindow, text="What would you like to name the playList?", bg="#191414", fg="#1DB954")
    createLabel.pack()

    global createEntry
    createEntry = Entry(createPlaylistWindow, bg="#696969")
    createEntry.pack()

    createButton = Button(createPlaylistWindow, text="Enter", command=playlist_creation, highlightbackground="#191414")
    createButton.pack()


def playlist_creation():
    new_playlist = createEntry.get()
    sp.user_playlist_create(user, new_playlist, True)

    playlist_completed_window = Tk()
    playlist_completed_window.geometry("300x200")
    playlist_completed_window.title('Create New Playlist')
    playlist_completed_window.config(bg="#191414")

    complete_label = Label(playlist_completed_window, text="Playlist Successfully Created", bg="#191414", fg="#1DB954", font="ProximaNova 20", pady=75)
    complete_label.pack()


def view_followed_artists():
    followed_artists = sp.current_user_followed_artists()

    artistsWindow = Tk()
    artistsWindow.geometry("400x400")
    artistsWindow.config(bg="#191414")
    artistsWindow.title('Followed Artists')
    artistsList = ""

    for x in followed_artists["artists"]["items"]:
        artists = x["name"]
        artistsList += artists
        artistsList += "\n"
    artistMessage = Label(artistsWindow, text="Artists\n" + artistsList, bg="#191414", fg="#1DB954")
    artistMessage.pack()

def checklist_maker(checker):
    checkerButton = Checkbutton(addPlaylistWindow, command=checker.toggle, text=checker.name, bg="#191414", fg="#1DB954", variable=checker.name)
    checkerButton.pack()

def checklist_maker_remove(checker):
    checkerButton = Checkbutton(removePlaylistWindow, command=checker.toggle, text=checker.name, bg="#191414", fg="#1DB954", variable=checker.name)
    checkerButton.pack()



def recent_checklist():
    playlistPrompt.config(text="Which song/songs would you like to add")
    global playlist
    playlist = playlistEntry.get()
    playlistEntry.destroy()
    global list
    list = []
    Songs = sp.current_user_recently_played()
    global song_id
    song_id = {}
    for x in Songs["items"]:
        name = x["track"]["name"]
        id = x["track"]["id"]
        song_id[name] = id
        list.append(name)

    global recentSongClass

    class recentSongClass:
        def __init__(self, songName):
            self.name = songName
            self.control = False

        def toggle(self):
            if(self.control == False):
                self.control = True
            else:
                self.control = False




    global recentSongList
    recentSongList = []

    for j in range(50):
        recentSongList.append(recentSongClass(list[j]))
        checklist_maker(recentSongList[j])

    enterButton.config(command=add_songs)
    enterButton.pack()



def add_songs():
    newList = []
    for i in range(50):
        if recentSongList[i].control:
            newList.append(recentSongList[i].name)
    randomList = []
    #playlist = playlistEntry.get()
    for i in range(len(newList)):
        idOfSong = song_id[newList[i]]
        randomList.append(idOfSong)

    sp.playlist_add_items(playlist_id[playlist], randomList)

    addSongSuccess = Tk()
    addSongSuccess.config(bg="#191414")
    addSongSuccess.title('Spotify App')
    addSongSuccess.geometry('400x150')

    successLabel = Label(addSongSuccess, text="Songs Successfully Added", fg="#1DB954", bg="#191414", font="ProximaNova 20")
    successLabel.pack()



global add_items_to_playlist
def add_items_to_playlist():
    try:
        global addPlaylistWindow
        addPlaylistWindow = Tk()
        addPlaylistWindow.config(bg="#191414")
        addPlaylistWindow.geometry("400x400")
        addPlaylistWindow.title('Add Songs To Playlist')

        global playlistPrompt
        playlistPrompt = Label(addPlaylistWindow, text="Which playlist would you like to add songs to?", bg="#191414", fg="#1DB954")
        playlistPrompt.pack()

        global playlistEntry
        playlistEntry = Entry(addPlaylistWindow, bg="#696969")
        playlistEntry.pack()

        global enterButton
        enterButton = Button(addPlaylistWindow, text="Enter", command=recent_checklist, highlightbackground="#191414")
        enterButton.pack()

    except:
        popUp = Tk()
        popUp.config(bg="#191414")
        popUp.geometry("200x50")
        popUp.title('Error')
        message = Label(popUp, text="Playlist not found\n Try again", foreground="red", bg="#191414",
                           font="Arial 20")
        message.pack()

def remove_songs_from_playlist():
    try:
        global removePlaylistWindow
        removePlaylistWindow = Tk()
        removePlaylistWindow.config(bg="#191414")
        removePlaylistWindow.geometry("400x400")
        removePlaylistWindow.title('Remove Songs From Playlist')

        global playlistPrompt
        playlistPrompt = Label(removePlaylistWindow, text="Which playlist would you like to remove songs from?", bg="#191414", fg="#1DB954")
        playlistPrompt.pack()

        global playlistEntry
        playlistEntry = Entry(removePlaylistWindow, bg="#696969")
        playlistEntry.pack()

        global enterButton
        enterButton = Button(removePlaylistWindow, text="Enter", command=remove_songs, highlightbackground="#191414")
        enterButton.pack()

    except:
        popUp = Tk()
        popUp.config(bg="#191414")
        popUp.geometry("200x50")
        popUp.title('Error')
        message = Label(popUp, text="Playlist not found\n Try again", foreground="red", bg="#191414",
                           font="Arial 20")
        message.pack()


def remove_songs():
    playlistPrompt.config(text="Which songs would you like to remove")
    global request
    request = playlistEntry.get()
    playlistEntry.destroy()
    global list
    list = []
    removePlaylistID = playlist_id[request]
    playlistPrompt.config(text=request)
    global newPlaylist
    newPlaylist = sp.playlist(removePlaylistID)
    global song_id
    song_id = {}

    global newList
    newList = []

    for x in newPlaylist["tracks"]["items"]:
        track = x["track"]["name"]
        id = x["track"]["id"]
        song_id[track] = id
        list.append(track)

    class recentSongClass:
        def __init__(self, songName):
            self.name = songName
            self.control = False

        def toggle(self):
            if(self.control == False):
                self.control = True
            else:
                self.control = False

    global newSongList
    newSongList = []

    for j in range(len(list)):
        newList.append(recentSongClass(list[j]))
        checklist_maker_remove(newList[j])

    enterButton.config(command=remove_items)
    enterButton.pack()


def remove_items():
    tempList = []
    for i in range(len(list)):
        if newList[i].control:
            tempList.append(newList[i].name)
    IDList = []
    for i in range(len(tempList)):
        idOfSong = song_id[tempList[i]]
        IDList.append(idOfSong)

    sp.playlist_remove_all_occurrences_of_items(playlist_id[request], IDList)

    removeSongSuccess = Tk()
    removeSongSuccess.config(bg="#191414")
    removeSongSuccess.title('Spotify App')
    removeSongSuccess.geometry('400x150')

    successLabel = Label(removeSongSuccess, text="Songs Successfully Removed", fg="#1DB954", bg="#191414",
                         font="ProximaNova 20")
    successLabel.pack()

def add_image_to_playlist():
    addImageWindow = Tk()
    addImageWindow.config(bg="#191414")
    addImageWindow.title('Add Image to Playlist')
    addImageWindow.geometry('400x300')
    imagePlaylist = Label(addImageWindow, text="What playlist would you like to add an image to?", fg="#1DB954", bg="#191414",
                          font="ProximaNova 16")
    imagePlaylist.pack()
    global imagePlaylistEntry
    imagePlaylistEntry = Entry(addImageWindow, bg="#191414", fg="#1DB954")
    imagePlaylistEntry.pack()

    imagePlaylistButton = Button(addImageWindow, text="Enter", command=image_Prompt, highlightbackground="#191414")
    imagePlaylistButton.pack()

    #print("Go to this website to convert and copy Base64 data: https://onlinejpgtools.com/convert-jpg-to-base64")
    #print("Paste data image")
    #requestImage = input()
    #addInto = playlist_id[request]
    #sp.playlist_upload_cover_image(playlist_id=addInto, image_b64=requestImage)
    #print("Image added")
def callback(url):
    webbrowser.open_new(url)

def image_Prompt():
    imageWindow = Tk()
    imageWindow.config(bg="#191414")
    imageWindow.title('Add Image')
    imageWindow.geometry("400x300")

    imagePlaylist = imagePlaylistEntry.get()
    playlistPrompt = Label(imageWindow, text="What image would you like to add to " + imagePlaylist, fg="#1DB954", bg="#191414")
    playlistPrompt.pack()

    directionPrompt = Label(imageWindow, text="Go to this website to convert and copy Base64 data: ", fg="#1DB954", bg="#191414")
    directionPrompt.pack()

    websitePrompt = Label(imageWindow, text=r"https://onlinejpgtools.com/convert-jpg-to-base64", fg="#1F51FF", bg="#191414",cursor="hand2")
    websitePrompt.pack()

    websitePrompt.bind("<Button-1>", lambda e: callback("https://onlinejpgtools.com/convert-jpg-to-base64"))

    global baseEntry
    baseEntry = Entry(imageWindow, bg="#191414", fg="#1DB954")
    baseEntry.pack()

    baseButton = Button(imageWindow, text="Enter", command=add_image_function, highlightbackground="#191414")
    baseButton.pack()

def add_image_function():
    requestImage = baseEntry.get()
    addInto = playlist_id[imagePlaylistEntry.get()]
    sp.playlist_upload_cover_image(playlist_id=addInto, image_b64=requestImage)
    successWindow = Tk()
    successWindow.config(bg="#191414")
    successWindow.title("Success")
    successWindow.geometry("400x150")
    successLabel = Label(successWindow, text="Image Added Successfully", bg="#191414", fg="#1DB954", font="ProximaNova 20")
    successLabel.pack()


def returntoHome():
    window.destroy()
    window1 = Tk()
    window1.title('Spotify App')
    window1.config(bg="#191414")
    window1.geometry("400x300")
    greeting.grid(row=1, column=1)
while 1:
    temp = sp.user_playlists(user)
    for x in temp['items']:
        name = x['name']
        id = x['id']
        playlist_id[name] = id

    window = Tk()
    window.title('Spotify App')
    window.config(bg="#191414")
    window.geometry("400x300")

    global greeting
    greeting = Label(window, text="Spotify App\nCreated by Ben Stroup", foreground="#1DB954", background="#191414",padx=100, pady=10)
    greeting.grid(row=1, column=1)

    userLabel = Label(window, fg="#1DB954", bg="#191414", text="Enter your Username")
    userText = Entry(window, bg="#191414", fg="#1DB954")
    #user = userText.get()
    #sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    userLabel.grid(row=2, column=1)
    userText.grid(row=3, column=1)


    def update_to_main():
        userLabel.destroy()
        userText.destroy()
        global display_name
        display_name = ""
        for z in temp['items']:
            item = z['owner']['display_name']
            display_name = item

        userName = Label(window, text="Welcome " + display_name, foreground="#1DB954", background="#191414")
        userName.grid(row=0, column=1)
        greeting.config(text="What would you like to do?")
        startButton.config(text="View Followed Artists", command=view_followed_artists, activeforeground="#1DB954")
        viewPlaylist = Button(window, text="View Owned Playlists", command=viewOwnedPlaylist, activeforeground="#1DB954", highlightbackground="#191414")
        viewPlaylist.grid(row=3, column=1)
        createPlaylist = Button(window, text="Create Playlist", command=create_new_playlist, activeforeground="#1DB954", highlightbackground="#191414")
        createPlaylist.grid(row=5, column=1)
        addItemPlaylist = Button(window, text="Add Items To Playlist", command=add_items_to_playlist, activeforeground="#1DB954", highlightbackground="#191414")
        addItemPlaylist.grid(row=6, column=1)
        removeSongPlaylist = Button(window, text="Remove Items on Playlist", command=remove_songs_from_playlist, activeforeground="#1DB954", highlightbackground="#191414")
        removeSongPlaylist.grid(row=7, column=1)
        addImagePlaylist = Button(window, text="Add Image to a Playlist", command=add_image_to_playlist, activeforeground="#1DB954", highlightbackground="#191414")
        addImagePlaylist.grid(row=8, column=1)

    global viewOwnedPlaylist

    def viewOwnedPlaylist():
        newWindow = Tk()
        newWindow.title('Spotify App')
        newWindow.config(bg="#191414")
        newWindow.geometry("400x400")
        viewPlaylistLabel = Label(newWindow, text="Which playlist would you like to view?", fg="#1DB954", background="#191414")
        viewPlaylistLabel.pack()

        global entry
        entry = Entry(newWindow, bg="#696969")
        entry.pack()

        playlistDisplay = Button(newWindow, text="Enter", command=playlist_display, activeforeground="#1DB954", highlightbackground="#191414")
        playlistDisplay.pack()


    def playlist_display():
        name_var = entry.get()
        view_owned_playlists(name_var)


    global startButton
    startButton = Button(window, text="Start", command=update_to_main, activeforeground="#1DB954", highlightbackground="#191414")
    startButton.grid(row=4, column=1)

    window.mainloop()
    break
