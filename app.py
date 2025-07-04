from flask import Flask, render_template, request, redirect, url_for
from BetterSpotifyTest import Spotify
from ytMusicTest import Youtube, Track
import time

app = Flask(__name__)
youtube = Youtube()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/transfer", methods=["POST"])
def transfer():
    from_platform = request.form.get("platform")
    playlist_id = request.form.get("playlist_id")
    to_platform = request.form.get("platform1")

    transfer_playlists(from_platform, playlist_id, to_platform)

    return f"Converted from {from_platform} to {to_platform} using playlist ID: {playlist_id}"

@app.route("/liked", methods=["POST"])
def get_liked_songs():
    spotify = Spotify()
    liked_songs = spotify.get_liked_songs()
    name, desc, youtube_tracks = youtube.search(liked_songs)
    print(youtube.create_playlist(name, desc, youtube_tracks))

@app.route("/spotify-login")
def spotify_login():
    spotify = Spotify()
    return redirect(spotify.get_auth_url())

@app.route("/callback")
def spotify_callback():
    code = request.args.get("code")
    spotify = Spotify()
    token = spotify.exchange_code_for_token(code)
    return "Authorization successful! Token obtained."


def transfer_playlists(from_platform, playlist_id, to_platform):
    spotify = Spotify()
    tracks = []
    name = ""
    desc = ""

    print("From:", from_platform)
    print("To:", to_platform)
    print("Playlist ID:", playlist_id)

    if from_platform == "Spotify":
        tracks = spotify.get_playlist_tracks(playlist_id)
        name, desc = spotify.get_name_and_desc(playlist_id)
    elif from_platform == "YouTube":
        name, desc, tracks = youtube.get_playlists(playlist_id)

    # print("Playlist name:", name)
    # print("Description:", desc)
    # print("Tracks:", tracks)

    if to_platform == "Spotify":
        spotify_uris = []

        for track in tracks:
            result = spotify.search(track)
            time.sleep(0.1)
            if len(result) > 0:
                spotify_uris.append(result[0])
        
        new_playlist_id = spotify.create_playlist(name, desc, True)
        spotify.add_songs_to_playlist(spotify_uris, new_playlist_id)
    
    elif to_platform == 'YouTube':
        ids = youtube.search(tracks)
        print(youtube.create_playlist(name, desc, ids))

if __name__ == "__main__":
    app.run(debug=True)
