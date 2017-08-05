from kivy.uix.screenmanager import Screen
from ui.components.phone import (CallScreenActive, CallScreenDialling,
                                 CallScreenIncoming)


class PhoneScreen(Screen):

    def __init__(self, name, hfp):
        super().__init__(name=name)
        self.hfp = hfp
        self.active_call = None
        sm = self.ids.screenmanager
        sm.add_widget(CallScreenActive(name='active',
                                       hfp=self.hfp))
        sm.add_widget(CallScreenDialling(name='dialing',
                                         hfp=self.hfp))
        sm.add_widget(CallScreenIncoming(name='active',
                                         hfp=self.hfp))
        self.sm = sm

    def on_attention_change(self, instance, value):
        self.active_call = value[0]
        if self.active_call.status == 'alerting':
            self.sm.current = 'dialing'
        if self.active_call.status == 'dialing' or 'active' or 'incoming':
            self.sm.current = self.active_call.status
