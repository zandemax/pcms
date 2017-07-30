from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

class Phonebook(Screen):

    def __init__(self, name, pbap):
        super().__init__(name=name)
        self.pbap = pbap
        pbap.bind(loaded = self.get_data)

    def get_data(self, instance, value):
        data = []
        for i in self.pbap.phonebook:
            data.append({'value': i.n.value.family})
        self.rv.data = data
