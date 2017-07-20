from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import time


class HomeScreen(Screen):

    def __init__(self, name, app):
        super().__init__(name=name)

        self.app = app
        self.ids.statusbar.set_app(app)
        self.ids.statusbar.set_title('Home')

        self.ids.controlbar.ids.music.bind(on_press=self.on_music)
        self.ids.controlbar.ids.phone.bind(on_press=self.on_phone)
        self.ids.controlbar.ids.home.color = 1,1,1,1

        Clock.schedule_interval(self.on_tick, 1)

    def on_music(self, instance):
        self.app.set_active_screen('music')

    def on_phone(self, instance):
        self.app.set_active_screen('dialler')

    def on_tick(self, dt):
        self.ids.time.text = time.strftime('%H:%M')
        self.ids.date.text = time.strftime('%a, %d %B %Y')
