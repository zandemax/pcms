from kivy.uix.screenmanager import Screen
from kivy.event import EventDispatcher
from kivy.properties import StringProperty


class Dialler(Screen, EventDispatcher):

    number = StringProperty("")

    def __init__(self, name, telman, app):
        super().__init__(name=name)
        self.telman = telman
        self.app = app
        self.ids.one.bind(on_press=self.key_press)
        self.ids.two.bind(on_press=self.key_press)
        self.ids.three.bind(on_press=self.key_press)
        self.ids.four.bind(on_press=self.key_press)
        self.ids.five.bind(on_press=self.key_press)
        self.ids.six.bind(on_press=self.key_press)
        self.ids.seven.bind(on_press=self.key_press)
        self.ids.eight.bind(on_press=self.key_press)
        self.ids.nine.bind(on_press=self.key_press)
        self.ids.zero.bind(on_press=self.key_press)
        self.ids.delete.bind(on_press=self.on_delete)
        self.ids.start.bind(on_press=self.on_start)

        self.bind(number=self.on_number_change)

    def on_delete(self, instance):
        self.number = self.number[:-1]

    def on_music(self, instance):
        self.app.set_active_screen('musicscreen')

    def on_home(self, instance):
        self.app.set_active_screen('homescreen')

    def key_press(self, instance):
        self.number = self.number + instance.text

    def on_number_change(self, instance, value):
        self.ids.numdisplay.text = self.number

    def on_start(self, instance):
        self.telman.call(self.number)
