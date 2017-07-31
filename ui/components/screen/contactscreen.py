from kivy.uix.screenmanager import Screen


class ContactScreen(Screen):

    def __init__(self, name, pbap):
        super().__init__(name=name)
        self.pbap = pbap
