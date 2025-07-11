from ytmusicapi import YTMusic
import time

class Youtube:
    def __init__(self):
        self.ytmusic = YTMusic("browser.json")
        # print(self.ytmusic.get_playlist("PL9bUIJbr567sPBgw7uflPlObHx4tuuERU"))    

    def get_playlists(self, id):
        playlist = self.ytmusic.get_playlist(id, limit=1000)
        name, desc = playlist['title'], playlist['description']
        
        # Yield playlist info first
        yield {'type': 'playlist_info', 'name': name, 'description': desc}
        
        # Then yield tracks
        for track in playlist["tracks"]:
            # print(track)
            if not track['thumbnails']:
                append_track = Track(track['title'], track['artists'][0]['name'], "")
            else:
                append_track = Track(track['title'], track['artists'][0]['name'], track['thumbnails'][0]['url'])
            yield append_track
    
    def search(self, search_songs):
        filter = 'songs'
        ids = []
        print(search_songs)
        for i, song in enumerate(search_songs):
            song = song.toString()
            print(song)
            try:
                search_results = self.ytmusic.search(song, filter)
            except:
                return []
            
            if len(search_results) > 0:  
                ids.append(search_results[0]['videoId'])
                
            time.sleep(0.1)
        return ids
    
    def search_song(self, search_song):
        filter = 'songs'
        song = search_song.toString()
        try:
            search_results = self.ytmusic.search(song, filter)
        except:
            return []
        
        if len(search_results) > 0:  
            return search_results[0]['videoId']

    def create_playlist(self, name, description, ids):
        return self.ytmusic.create_playlist(name, description, "PUBLIC", video_ids=ids)

    def get_liked_songs(self):
        tracks = self.ytmusic.get_liked_songs(1000)
        result_tracks = []
        for i in tracks['tracks']:
            result_tracks.append(Track(i['title'], i['artists'][0]['name'], ""))

        return result_tracks

class Track:
    def __init__(self, title, artist, url):
        self.title = title
        self.artist = artist
        self.url = url
    
    def toString(self):
        return f"{self.title} {self.artist}"