from kivy.uix.screenmanager import Screen, NoTransition
from ui.components.phone import (CallScreenActive, CallScreenDialling,
                                 CallScreenIncoming)


class PhoneScreen(Screen):

    def __init__(self, name, hfp, pbap):
        super().__init__(name=name)
        self.hfp = hfp
        self.active_call = None
        sm = self.ids.screenmanager
        sm.add_widget(CallScreenActive(name='active',
                                       hfp=self.hfp, pbap=pbap))
        sm.add_widget(CallScreenDialling(name='dialing',
                                         hfp=self.hfp, pbap=pbap))
        sm.add_widget(CallScreenIncoming(name='active',
                                         hfp=self.hfp, pbap=pbap))
        sm.transition = NoTransition()
        self.sm = sm
        hfp.bind(attention=self.on_attention_change)

    def on_attention_change(self, instance, value):
        self.active_call = value[0]
        print(value[1])
        if value[1] is not None:
            if value[1] == 'alerting':
                self.sm.current = 'dialing'
            if value[1] == 'dialing' or value[1] == 'active' or value[1] == 'incoming':
                print('True!')
                self.sm.current = value[1]
                print(self.sm.current)
