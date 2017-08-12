from ui.components.phone.callscreen import CallScreen
from kivy.clock import Clock
from math import floor


class CallScreenActive(CallScreen):

    def __init__(self, name, hfp, pbap):
        super().__init__(name, hfp)
        self.clockstop = False
        self.calltime = 0
        self.hfp = hfp
        self.pbap = pbap
        Clock.schedule_interval(self.on_tick, 1)
        hfp.bind(attention=self.on_call_change)
        self.ids.end.bind(on_press=self.on_end)

    def on_call_change(self, instance, value):
        if value[0] is not None:
            try:
                self.ids.number.text = self.pbap.phonebook_search(value[0].line_id)
            except KeyError:
                self.ids.number.text = value[0].line_id

    def on_tick(self, dt):
        self.calltime = self.calltime+1
        calltime_string = str(floor(self.calltime/60)%60)+':'+str(floor(self.calltime)%60).zfill(2)
        self.ids.elapsed.text = calltime_string
        return self.clockstop

    def on_end(self, instance):
        self.parent.active_call.hangup()
