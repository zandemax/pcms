from kivy.uix.screenmanager import Screen
from ui.components.contacts import ContactViewItem, ContactViewDummy
#from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class ContactScreen(Screen):

    def __init__(self, name, pbap, hfp):
        super().__init__(name=name)
        self.pbap = pbap
        self.hfp = hfp
        self.scrollview = self.ids.scrollview
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.scrollview.add_widget(self.layout)
        self.pbap.bind(loaded=self.get_data)

    def get_data(self, instance, value):
        data = []
        child = ContactViewDummy(size_hint_y=None, height=50)
        self.layout.add_widget(child)
        for i in self.pbap.phonebook:
            child = ContactViewItem(name=i.fn.value, number=i.tel.value, size_hint_y=None, height=100)
#            child = Button(text=str(i), size_hint_y=None, height=40)
            self.layout.add_widget(child)
        child = ContactViewDummy(size_hint_y=None, height=50)
        self.layout.add_widget(child)

    def call(self, instance):
        self.hfp.call(instance.number)
