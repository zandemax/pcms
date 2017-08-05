from kivy.uix.relativelayout import RelativeLayout


kv = '''

<ProgressBarColor>
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Circle:
            pos: 100, 100
            size: 10, 10
            source: 'data/logo/kivy-icon-512.png'
            angle_start: e1.value
            angle_end: e2.value

class ProgressBarColor(RelativeLayout):

    value = NumericProperty()

    def __init__(self):
        self.value = 0
        self.bind(value=self.on_value_change)

    def on_value_change(self, instance, value):
        if value > 1:
            value = 1
        elif value < 0:
            value = 0
        self.ids.elapsed.width = self.width / value
