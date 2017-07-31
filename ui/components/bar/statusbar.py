from kivy.uix.widget import Widget
from kivy.clock import Clock
import time
from kivy.logger import Logger


class StatusBar(Widget):

    def __init__(self, **args):
        super().__init__()
        Clock.schedule_interval(self.on_tick, 1)
        self.app = None
        Logger.info('Statusbar ('+str(self.parent)+'): Init')

    def set_app(self, app):
        self.app = app
        app.a2dp.bind(connected=self.on_connected_change)
        app.hfp.bind(carrier=self.on_carrier_change)
        app.hfp.bind(network_strength=self.on_signal_change)
        app.hfp.bind(connected=self.on_hfp_connected_change)
        self.on_connected_change('', '')
        self.on_carrier_change('', '')
        self.on_signal_change('', '')
        Logger.info('Statusbar ('+str(self.parent)+'): App set')

    def on_tick(self, dt):
        self.ids.time.text = time.strftime('%H:%M')

    def on_connected_change(self, instance, value):
        if value is True:
            self.ids.bluetooth.source = '/home/zandemax/coding/pcms/img/icon_bluetooth_connected.png'
        else:
            self.ids.bluetooth.source = '/home/zandemax/coding/pcms/img/icon_bluetooth.png'

    def on_hfp_connected_change(self, instance, value):
        if value is False:
            self.ids.cellular.source = '/home/zandemax/coding/pcms/img/icon_cellular_off.png'
            self.ids.carrier.text = 'no carrier'

    def on_signal_change(self, instance, value):
        if self.app.hfp.network_strength == 0:
            self.ids.cellular.source = '/home/zandemax/coding/pcms/img/icon_cellular_nonet.png'
            self.ids.cellular.reload()
        else:
            self.ids.cellular.source = '/home/zandemax/coding/pcms/img/icon_cellular_connected.png'
            self.ids.cellular.reload()
        Logger.info('Statusbar ('+str(self.parent)+'): Update')

    def on_carrier_change(self, instance, value):
        if self.app.hfp.carrier is not None:
            self.ids.carrier.text = self.app.hfp.carrier
        else:
            self.ids.carrier.text = 'no carrier'

    def set_title(self, title):
        self.ids.title.text = title
