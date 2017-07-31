from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout


class ContactView(RecycleView):

    def __init__(self, **kwargs):
        super(ContactView, self).__init__(**kwargs)
        self.viewclass = ContactViewItem
        self.pbap = self.parent.pbap
        self.pbap.bind(loaded=self.get_data)

    def get_data(self, instance, value):
        data = []
        for i in self.pbap.phonebook:
            data.append({'value': i.fn.value})
        self.data = data


class ContactViewItem(RecycleDataViewBehavior, ButtonBehavior, RelativeLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_press = self.on_button_press

    def on_button_press(self, instance):
        pass
