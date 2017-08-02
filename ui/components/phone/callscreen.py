from kivy.uix.screenmanager import Screen


class CallScreen(Screen):

    def __init__(self, name, hfp):
        super().__init__(name=name)
        self.hfp = hfp
        #hfp.bind(active_call=self.on_call_change)

    def on_call_change(self, instance, value):
        self.ids.number.text = value['properties']['LineIdentification']

    def end_call(self):
        self.hfp.end_call(self.hfp.active_call)
