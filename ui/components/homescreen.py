from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import time


class HomeScreen(Screen):

    def __init__(self, name, app):
        super().__init__(name=name)
        self.app = app
        Clock.schedule_interval(self.on_tick, 1)

    def on_music(self, instance):
        self.app.set_active_screen('music')

    def on_phone(self, instance):
        self.app.set_active_screen('dialler')

    def on_tick(self, dt):
        self.ids.time.text = time.strftime('%H:%M')
        self.ids.date.text = time.strftime('%a, %d %B %Y')
