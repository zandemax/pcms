from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from helpers.weather import WeatherHelper
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
import time


class HomeScreen(Screen, EventDispatcher):

    iconname = StringProperty('wi-day-cloudy')

    def __init__(self, name, app):
        super().__init__(name=name)
        self.app = app
        Clock.schedule_interval(self.on_tick, 1)
#        weatherhelper = WeatherHelper()
#        weather = weatherhelper.get_weather('Munich,DE')
#        self.ids.temperature.text = str("%.1f" % round(weather['temp'],
#                                                       2))+'°C'
#        self.ids.weathertext.text = weather['dstatus']
#        self.iconname = weatherhelper.icons[weather['status']]
#        print(weather['status'])

    def on_tick(self, dt):
        self.ids.time.text = time.strftime('%H:%M')
        self.ids.date.text = time.strftime('%a, %d %B %Y')
