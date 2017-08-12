from helpers import pygn


class AlbumArtHelper():

    def __init__(self):
        self.client_id = '83438401-F69672F5A5835CC4A7162991B9FD2882'
        self.user_id = pygn.register(self.client_id)

    def get_albumart_url(self, artist, track):
        print(artist)
        print(track)
        metadata = pygn.search(clientID=self.client_id, userID=self.user_id, artist=artist, track=track)
        if metadata is not None:
            print(metadata)
            url = metadata['album_art_url']
            return url
        return KeyError
