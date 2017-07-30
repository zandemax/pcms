from kivy.uix.widget import Widget

class ControlBar(Widget):

    def __init__(self, **args):
        super().__init__()

    def set_active_icon(self, screen):
        if screen = 'homescreen':
            self.ids.home.color = 1,1,1,1
            self.ids.phone.color = .7,.7,.7,1
            self.ids.music.color = .7,.7,.7,1
        if screen = 'phonebook':
            self.ids.home.color = .7,.7,.7,1
            self.ids.phone.color = 1,1,1,1
            self.ids.music.color = .7,.7,.7,1
        if screen = 'music':
            self.ids.home.color = .7,.7,.7,1
            self.ids.phone.color = .7,.7,.7,1
            self.ids.music.color = 1,1,1,1
