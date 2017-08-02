from ui.components.phone.callscreen import CallScreen
from kivy.clock import Clock


class CallScreenDialling(CallScreen):

    def __init__(self, name, hfp):
        super().__init__(name, hfp)
        self.x = 0
        Clock.schedule_interval(self.on_timeout, 1)

    def on_timeout(self, dt):
        self.x = self.x + 1
        if self.x <= 3:
            self.ids.dialling.text = self.ids.dialling.text + '.'
        else:
            self.ids.dialling.text = "dialling"
            self.x = 0
