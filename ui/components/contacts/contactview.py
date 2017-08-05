from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty


class ContactView(RecycleView):

    def __init__(self, **kwargs):
        super(ContactView, self).__init__(**kwargs)
        self.viewclass = ContactViewItem
        self.pbap = None
        self.get_data('','')

    def set_pbap(self, pbap):
        self.pbap = pbap
        self.pbap.bind(loaded=self.get_data)

    def get_data(self, instance, value):
        data = []
        for i in range(0, 10):  #self.pbap.phonebook:
            data.append({'name': 'i.fn.value', 'number': '00000000000000'})
        self.data = data


class ContactViewItem(RecycleDataViewBehavior, ButtonBehavior, RelativeLayout):

    number = StringProperty()
    name = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_press = self.on_button_press

    def on_button_press(self):
        print('Button pressed!!!!!')
