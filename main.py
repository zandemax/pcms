from ui.ui import UserInterface
from kivy.garden.iconfonts import iconfonts

from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

iconfonts.register('weather', 'img/weathericons-regular-webfont.ttf', 'img/weather_icons.fontd')
UserInterface().run()
