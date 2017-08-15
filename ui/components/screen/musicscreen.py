from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from math import floor
from kivy.logger import Logger
#from helpers.albumart import AlbumArtHelper


class MusicScreen(Screen):

    def __init__(self, name, a2dp, app):
        super().__init__(name=name)
#        self.arthelper = AlbumArtHelper()
        self.a2dp = a2dp
        self.app = app
        a2dp.bind(title=self.on_title_change)
        a2dp.bind(artist=self.on_artist_change)
        a2dp.bind(duration=self.on_duration_change)
        a2dp.bind(connected=self.on_connected_change)
        self.ids.next.bind(on_press=self.on_next)
        self.ids.prev.bind(on_press=self.on_previous)
        self.ids.play.bind(on_press=self.on_play)
        self.fetch_current_data()
        self.on_connected_change(self, self.a2dp.connected)
        Clock.schedule_interval(self.progress_callback, 0.05)

    def on_title_change(self, instance, value):
        Logger.info('Music: Title changed')
        if len(self.a2dp.title) <= 40:
            self.ids.title.text = self.a2dp.title
        else:
            self.ids.title.text = self.a2dp.title[:36]+'...'
#        try:
#            url = self.arthelper.get_albumart_url(self.a2dp.title, self.a2dp.artist)
#            if url is not KeyError:
#                self.ids.image.source = url
#        except KeyError:
#            pass

    def on_artist_change(self, instance, value):
        self.ids.artist.text = self.a2dp.artist

    def on_duration_change(self, instance, value):
        self.ids.duration.text = str(floor(
            self.a2dp.duration/(1000*60)) % 60)+':'+str(floor(
                self.a2dp.duration/1000) % 60).zfill(2)

    def fetch_current_data(self):
        # TODO: Refactor to use comprehensible syntax
        self.on_duration_change('', '')
        self.on_artist_change('', '')
        self.on_title_change('', '')

    def on_connected_change(self, instance, value):
        if value is False:
            self.ids.title.text = 'No Device'
            self.ids.artist.text = 'No Device'
            self.ids.play.source = '/home/zandemax/coding/pcms/img/icon_play_circle_o.png'

    def on_next(self, instance):
        print('next pressed')
        self.a2dp.next()

    def on_previous(self, instance):
        self.a2dp.previous()

    def on_play(self, instance):
        Logger.info('Music: Play pressed')
        if self.a2dp.status == 'paused':
            self.a2dp.play()
            self.ids.play.source = '/home/zandemax/coding/pcms/img/icon_pause_circle_o.png'
        else:
            self.a2dp.pause()
            self.ids.play.source = '/home/zandemax/coding/pcms/img/icon_play_circle_o.png'

    def progress_callback(self, dt):
        if self.a2dp.status == 'playing':
            self.a2dp.current_pos = self.a2dp.current_pos + dt
            self.ids.elapsed.text = str(floor(self.a2dp.current_pos/(1000*60))%60)+':'+str(floor(self.a2dp.current_pos/1000)%60).zfill(2)
            try:
                self.ids.progressbar.value = (self.a2dp.current_pos/self.a2dp.duration)*100
            except ZeroDivisionError:
                pass
            return True
        else:
            return True
