from kivy.uix.screenmanager import Screen
from ui.components.contacts import ContactView


class ContactScreen(Screen):

    def __init__(self, name, pbap):
        super().__init__(name=name)
        self.pbap = pbap
        self.ids.contactview.set_pbap(self.pbap)
