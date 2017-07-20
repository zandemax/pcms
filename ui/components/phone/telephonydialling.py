from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

class TelephonyDialling(Screen):

    def __init__(self, name, telman):
        super().__init__(name=name)
        self.telman = telman
        telman.bind(active_call=self.on_call_change)
        self.x = 0
        Clock.schedule_interval(self.on_timeout, 1)

    def on_call_change(self, instance, value):
        self.ids.number.text = value['properties']['LineIdentification']

    def on_timeout(self, dt):
        self.x = self.x + 1
        if self.x <= 3:
            self.ids.dialling.text = self.ids.dialling.text + '.'
        else:
            self.ids.dialling.text = "dialling"
            self.x = 0
