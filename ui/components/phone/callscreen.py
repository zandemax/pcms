from kivy.uix.screenmanager import Screen


class CallScreen(Screen):

    def __init__(self, name, hfp):
        super().__init__(name=name)
        self.hfp = hfp

    def end_call(self):
        self.hfp.end_call(self.hfp.active_call)
