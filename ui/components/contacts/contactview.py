from kivy.uix.button import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty


class ContactViewItem(ButtonBehavior, RelativeLayout):

    number = StringProperty()
    name = StringProperty()

    def __init__(self, name, number, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.number = number
        self.on_press = self.on_button_press

    def on_button_press(self):
        self.parent.parent.parent.call(self)

class ContactViewDummy(RelativeLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
