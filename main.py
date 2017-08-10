from ui.ui import UserInterface
from kivy.garden.iconfonts import iconfonts
from kivy import resources

from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

resources.resource_add_path('/home/zandemax/coding/pcms/img/defaulttheme-0.png')
resources.resource_remove_path('/usr/lib/python3.6/site-packages/kivy/data/images/defaulttheme-0.png')
print(resources.resource_find('defaulttheme-0'))


iconfonts.register('weather', 'img/weathericons-regular-webfont.ttf', 'img/weather_icons.fontd')
UserInterface().run()
