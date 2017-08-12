from kivy.uix.screenmanager import Screen
import can


class SettingsScreen(Screen):

    def __init__(self, name):
        super().__init__(name=name)
        self.ids.power.bind(on_press=self.on_power)

    def on_power(self, instance):
        bus = can.interface.Bus('infotainment', bustype='virtual')
        msg1 = can.Message(arbitration_id=0x1D6, data=[0xC1, 0x0C])
        bus.send(msg1)
        print('message sent:'+str(msg1))
