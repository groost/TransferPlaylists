import requests
import base64
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs
from ytMusicTest import Track

class Spotify:
    def __init__(self):
        self.client_id = '38dea9d3a01744aea205b2d60761f2f9'
        self.client_secret = '55e266eea7494b12a279e1e1586adec9'
        self.redirect_uri = "http://localhost:8888/callback"
        self.user_id = ""

        # self.authorize()
        # auth_str = f"{self.client_id}:{self.client_secret}"
        # b64_auth_str = base64.b64encode(auth_str.encode()).decode()

        # headers = {
        #     "Authorization": f"Basic {b64_auth_str}",
        # }

        # data = {
        #     "grant_type": "client_credentials",
        # }

        # response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

        # self.token = response.json()["access_token"]

    def get_auth_url(self):
        scopes = "playlist-modify-private playlist-modify-public user-library-read"
        params = urlencode({
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scopes,
        })

        return f"https://accounts.spotify.com/authorize?{params}"


    def exchange_code_for_token(self, code):
        token_url = "https://accounts.spotify.com/api/token"
        auth_str = f"{self.client_id}:{self.client_secret}"
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_auth_str}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }

        response = requests.post(token_url, headers=headers, data=data)
        response_data = response.json()
        self.token = response_data["access_token"]

        headers = {"Authorization": f"Bearer {self.token}"}
        user_profile = requests.get("https://api.spotify.com/v1/me", headers=headers).json()
        self.user_id = user_profile["id"]
        print("DONE")
        return self.token

    def authorize(self):
        scopes = "playlist-modify-private playlist-modify-public user-library-read"
        params = urlencode({
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scopes,
        })

        auth_url = f"https://accounts.spotify.com/authorize?{params}"
        print(f"Go to the following URL to authorize:\n{auth_url}")
        webbrowser.open(auth_url)

        redirected_url = input("Paste the full redirect URL here:\n")
        code = parse_qs(urlparse(redirected_url).query)["code"][0]

        token_url = "https://accounts.spotify.com/api/token"
        auth_str = f"{self.client_id}:{self.client_secret}"
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_auth_str}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }

        response = requests.post(token_url, headers=headers, data=data)
        response_data = response.json()
        self.token = response_data["access_token"]

        headers = {"Authorization": f"Bearer {self.token}"}
        user_profile = requests.get("https://api.spotify.com/v1/me", headers=headers).json()
        self.user_id = user_profile["id"]

    def get_playlist_tracks(self, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        all_tracks = []
        while url:
            res = requests.get(url, headers=headers)
            data = res.json()

            for item in data["items"]:
                track = item["track"]
                all_tracks.append(Track(track['name'], track['artists'][0]['name'], track['album']['name']))

            url = data["next"]

        return all_tracks
    
    def get_name_and_desc(self, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        res = requests.get(url, headers=headers)
        data = res.json()

        return data['name'], data['description']
    
    def create_playlist(self, name, description, public=False):
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        data = {
            "name": name,
            "description": description,
            "public": public
        }
        print(data)
        response = requests.post(url, headers=headers, json=data)
        # print(response.json())
        return response.json()['id']
    
    def get_liked_songs(self):
        url = "https://api.spotify.com/v1/me/tracks?limit=50"
        headers = {"Authorization": f"Bearer {self.token}"}
        liked = []

        while url:
            res = requests.get(url, headers=headers)
            data = res.json()
            for item in data.get("items", []):
                track = item["track"]
                liked.append(Track(track['name'], track['artists'][0]['name'], track['album']['name']))
                # print(liked[-1])
            url = data.get("next")  # next page

        return liked

    def add_songs_to_playlist(self, song_ids, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        data = {
            "uris": song_ids
        }

        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            print("Tracks added successfully.")
        else:
            print("Failed to add tracks:", response.status_code, response.text)

    def search(self, track):
        url = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        params = {
            "q": f"track:\"{track.title}\" artist:\"{track.artist}\"",      # e.g. "track:Yellow artist:Coldplay"
            "type": "track",
            "limit": 1
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        tracks = data.get("tracks", {}).get("items", [])
        uris = [track["uri"] for track in tracks]
        return uris