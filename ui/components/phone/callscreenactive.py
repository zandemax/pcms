from ui.components.phone.callscreen import CallScreen
from kivy.clock import Clock
from math import floor


class CallScreenActive(CallScreen):

    def __init__(self, name, hfp):
        super().__init__(name, hfp)
        self.hfp = hfp
        #hfp.bind(active_call=self.on_call_change)
        #hfp.bind(status=self.on_status_change)
        self.clockstop = True
        self.calltime = 0

    def on_call_change(self, instance, value):
        self.ids.number.text = value['properties']['LineIdentification']

    def on_status_change(self, instance, value):
        if value == 'active':
            self.clockstop = False
            self.calltime = 0
            Clock.schedule_interval(self.on_tick, 1)
        else:
            self.clockstop = True

    def on_tick(self, dt):
        self.calltime = self.calltime+1
        calltime_string = str(floor(self.calltime/60)%60)+':'+str(floor(self.calltime)%60).zfill(2)
        self.ids.elapsed.text = calltime_string
        return self.clockstop
