from urllib.parse import urlparse, parse_qs
from flask import Flask, Response, jsonify, render_template, request, redirect, url_for
from BetterSpotifyTest import Spotify
from ytMusicTest import Youtube, Track
import time
import json

application = Flask(__name__)
youtube = Youtube()
spotify = Spotify()

@application.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@application.route("/transfer-html", methods=["GET"])
def transfer_html():
    return render_template("playlists.html")

@application.route("/transfer", methods=["POST"])
def transfer():
    from_platform = request.form.get("platform")
    playlist_id = request.form.get("playlist_id")
    to_platform = request.form.get("platform1")
    
    def generate():
        try:
            tracks = []
            name = ""
            desc = ""

            if from_platform == "Spotify":
                track_generator = spotify.get_playlist_tracks(playlist_id)
                
                for track in track_generator:
                    # track_data = {
                    #     'name': track.title,
                    #     'artist': track.artist,
                    #     'image': track.url
                    # }
                    # yield f"data: {json.dumps(track_data)}\n\n"
                    tracks.append(track)
                
                name, desc = spotify.get_name_and_desc(playlist_id)
                
            elif from_platform == "YouTube":
                track_generator = youtube.get_playlists(playlist_id)
                playlist_info = next(track_generator)
                name = playlist_info['name']
                desc = playlist_info['description']
                for track in track_generator:
                    # track_data = {
                    #     'name': getattr(track, 'title', str(track)),
                    #     'artist': getattr(track, 'artist', 'Unknown'),
                    #     'image': getattr(track, 'url', '')
                    # }
                    tracks.append(track)
                    # yield f"data: {json.dumps(track_data)}\n\n"

            # Transfer phase (no yielding here)
            if to_platform == "Spotify":
                spotify_uris = []
                
                for track in tracks:
                    result = spotify.search(track)
                    time.sleep(0.1)
                    if len(result) > 0:
                        spotify_uris.append(result[0])

                    track_data = {
                        'name': track.title,
                        'artist': track.artist,
                        'image': track.url
                    }

                    yield f"data: {json.dumps(track_data)}\n\n"  
                
                new_playlist_id = spotify.create_playlist(name, desc, True)
                print(new_playlist_id)
                spotify.add_songs_to_playlist(spotify_uris, new_playlist_id)
            
            elif to_platform == 'YouTube':
                ids = []
                for track in tracks:
                    id = youtube.search_song(track)
                    time.sleep(0.1)
                    ids.append(id)
                    
                    track_data = {
                        'name': track.title,
                        'artist': track.artist,
                        'image': track.url
                    }

                    yield f"data: {json.dumps(track_data)}\n\n"
                    
                youtube.create_playlist(name, desc, ids)
            
            # Send completion signal
            yield f"data: {json.dumps({'completed': True})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@application.route("/liked", methods=["POST"])
def get_liked_songs():
    platform = request.form.get("liked_select")
    if platform == "Youtube":
        liked_songs = youtube.get_liked_songs()
        uris = spotify.search_songs(liked_songs)
        new_playlist_id = spotify.create_playlist("liked songs", "", True)
        spotify.add_songs_to_playlist(uris, new_playlist_id)
    else:
        liked_songs = spotify.get_liked_songs()
        # print(liked_songs)
        youtube_tracks = youtube.search(liked_songs)
        # print(youtube_tracks)
        print(youtube.create_playlist("liked songs1", "", youtube_tracks))
        
    return render_template("index.html")


@application.route("/spotify-login")
def spotify_login():
    return redirect(spotify.get_auth_url())

@application.route("/submit_redirect_url", methods=["POST"])
def submit_redirect_url():
    redirect_url = request.form.get("redirect_url")

    parsed_url = urlparse(redirect_url)
    code = parse_qs(parsed_url.query).get("code", [None])[0]

    if not code:
        return "Invalid URL. Could not find authorization code.", 400

    spotify.exchange_code_for_token(code)

    return render_template("index.html")

@application.route("/callback")
def spotify_callback():
    code = request.args.get("code")
    token = spotify.exchange_code_for_token(code)
    return "Authorization successful! Token obtained."

@application.route("/get_playlist")
def get_playlist_items():
    playlist_id = request.form.get("playlist_id")
    tracks = []
    check = spotify.get_playlist_tracks(playlist_id)
    while not check is None:
        tracks.append(check)

@application.route('/api/playlist/<playlist_id>/tracks/stream')
def stream_playlist_tracks(playlist_id):
    """
    Server-Sent Events endpoint for real-time streaming
    """

    try:
        return application.response_class(
            spotify.get_playlist_tracks_streaming(playlist_id),
            mimetype='text/event-stream'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

if __name__ == "__main__":
    application.run(debug=True)
