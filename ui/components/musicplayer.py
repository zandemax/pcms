from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from math import floor
from kivy.logger import Logger

class MusicPlayer(Screen):

    def __init__(self, name, a2dp, app):
        super().__init__(name=name)
        self.a2dp = a2dp
        self.app = app
        a2dp.bind(title=self.on_title_change)
        a2dp.bind(artist=self.on_artist_change)
        a2dp.bind(duration=self.on_duration_change)
        a2dp.bind(connected=self.on_connected_change)
        self.ids.next.bind(on_press=self.on_next)
        self.ids.prev.bind(on_press=self.on_previous)
        self.ids.play.bind(on_press=self.on_play)

        self.ids.statusbar.set_app(app)
        self.ids.statusbar.set_title('Music')
        print(self.ids.statusbar)
        Logger.info('Music: Statusbar set')

        self.ids.controlbar.ids.phone.bind(on_press=self.on_dialler)
        self.ids.controlbar.ids.home.bind(on_press=self.on_home)
        self.ids.controlbar.ids.music.color = 1,1,1,1

        self.fetch_current_data()

        Clock.schedule_interval(self.progress_callback, 0.05)

#### MUSIC ####

    def on_title_change(self, instance, value):
        Logger.info('Music: Title changed')
        self.ids.title.text = self.a2dp.title

    def on_artist_change(self, instance, value):
        self.ids.artist.text = self.a2dp.artist

    def on_duration_change(self, instance, value):
        self.ids.duration.text = str(floor(self.a2dp.duration/(1000*60))%60)+':'+str(floor(self.a2dp.duration/1000)%60).zfill(2)

    def fetch_current_data(self):
        self.on_duration_change('', '')
        self.on_artist_change('', '')
        self.on_title_change('', '')

    def on_connected_change(self, instance, value):
        if value == False:
            self.ids.artist.text = 'No Device'
            self.ids.play.source = '/home/zandemax/coding/pcms/img/icon_play_circle.png'


#### CONTROL BAR #####

    def on_dialler(self, instance):
        self.parent.transition.direction = "left"
        self.app.set_active_screen('dialler')

    def on_home(self, instance):
        self.app.set_active_screen('homescreen')

    def on_next(self, instance):
        print('next pressed')
        self.a2dp.next()

    def on_previous(self, instance):
        self.a2dp.previous()

    def on_play(self, instance):
        Logger.info('Music: Play pressed')
        if self.a2dp.status == 'paused':
            self.a2dp.play()
            self.ids.play.source = '/home/zandemax/coding/pcms/img/icon_pause_circle.png'
        else:
            self.a2dp.pause()
            self.ids.play.source = '/home/zandemax/coding/pcms/img/icon_play_circle.png'


    def progress_callback(self, dt):
        if self.a2dp.status == 'playing':
            self.a2dp.current_pos = self.a2dp.current_pos + 50
            elapsed_label = str(floor(self.a2dp.current_pos/(1000*60))%60)+':'+str(floor(self.a2dp.current_pos/1000)%60).zfill(2)
            self.ids.elapsed.text = elapsed_label
            try:
                new_value = (self.a2dp.current_pos/self.a2dp.duration)*100
        #            print(self.tracktime)
        #            print(self.currenttime)
        #            print(new_value)
                self.ids.progressbar.value = new_value
            except ZeroDivisionError:
                pass
            return True
        else:
            return True
