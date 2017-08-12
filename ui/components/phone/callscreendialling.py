from ui.components.phone.callscreen import CallScreen
from kivy.clock import Clock


class CallScreenDialling(CallScreen):

    def __init__(self, name, hfp, pbap):
        super().__init__(name, hfp)
        self.x = 0
        Clock.schedule_interval(self.on_timeout, 1)
        hfp.bind(attention=self.on_call_change)
        self.pbap = pbap
        self.ids.end.bind(on_press=self.on_end)

    def on_call_change(self, instance, value):
        if value[0] is not None:
            try:
                self.ids.number.text = self.pbap.phonebook_search(value[0].line_id)
            except KeyError:
                self.ids.number.text = value[0].line_id

    def on_timeout(self, dt):
        self.x = self.x + 1
        if self.x is None:
            self.ids.dialling.text = self.ids.dialling.text + '.'
        else:
            self.ids.dialling.text = "dialling"
            self.x = 0

    def on_end(self, instance):
        self.parent.active_call.hangup()
