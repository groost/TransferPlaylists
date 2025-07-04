from ytmusicapi import YTMusic
import time

class Youtube:
    def __init__(self):
        self.ytmusic = YTMusic("headers_auth.json")
        # print(self.ytmusic.get_playlist("PL9bUIJbr567sPBgw7uflPlObHx4tuuERU"))    

    def get_playlists(self, id):
        playlist = self.ytmusic.get_playlist(id, limit=1000)
        # print(json.dumps(playlist, indent=2))
        name, desc = playlist['title'], playlist['description']
        # print(name, desc)
        all_tracks = []

        for track in playlist["tracks"]:
            if not track['album']:
                all_tracks.append(Track(track['title'], track['artists'][0]['name'], ""))
            else:
                all_tracks.append(Track(track['title'], track['artists'][0]['name'], track['album']['name']))

        return name, desc, all_tracks
    
    def search(self, search_songs):
        filter = 'songs'
        ids = []
        print(search_songs)
        for i, song in enumerate(search_songs):
            song = song.toString()
            print(song)
            ids.append(self.ytmusic.search(song, filter)[0]['videoId'])
            time.sleep(0.1)
        return ids

    def create_playlist(self, name, description, ids):
        return self.ytmusic.create_playlist(name, description, "PUBLIC", video_ids=ids)

class Track:
    def __init__(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album
    
    def toString(self):
        return f"{self.title} {self.artist}"