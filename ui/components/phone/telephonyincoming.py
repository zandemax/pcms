from kivy.uix.screenmanager import Screen

class TelephonyIncoming(Screen):

    def __init__(self, name, telman):
        super().__init__(name=name)
        self.telman = telman
        telman.bind(active_call=self.on_call_change)

    def on_call_change(self, instance, value):
        self.ids.number.text = value['properties']['LineIdentification']
