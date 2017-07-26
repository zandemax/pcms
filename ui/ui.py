from threading import Thread
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivy.support import install_gobject_iteration
from dbushelpers.a2dp import A2DPManager
from dbushelpers.hfp import HFPManager
from dbushelpers.bluetooth import BluetoothManager
from dbushelpers.pbap import PhonebookManager
from ui.components import *
from ui.components.phone.phonebook import Phonebook
from kivy.logger import Logger


class UserInterface(App):

    def build(self):
        install_gobject_iteration()

        self.bluetooth = BluetoothManager()
        self.hfp = HFPManager(self.bluetooth)
        self.a2dp = A2DPManager(self.bluetooth)
        self.pbap = PhonebookManager(self.bluetooth)

        self.a2dp.bind(connected=self.on_connected_change)
        self.hfp.bind(status=self.on_call_status_change)

##### UI ######
        screenmanager = ScreenManager()
        self.musicplayer = MusicPlayer(name='music', a2dp=self.a2dp, app=self)
        screenmanager.add_widget(self.musicplayer)
#        screenmanager.add_widget(TelephonyIncoming(name='telephony_incoming', hfp=self.hfp))
#        screenmanager.add_widget(TelephonyDialling(name='telephony_dialling', hfp=self.hfp))
#        screenmanager.add_widget(TelephonyActive(name='telephony_active', hfp=self.hfp))
#        screenmanager.add_widget(Dialler(name='dialler', hfp=self.hfp, app=self))
        screenmanager.add_widget(Phonebook(name='phonebook', pbap=self.pbap))
        screenmanager.add_widget(HomeScreen(name='homescreen', app=self))
        screenmanager.current = 'phonebook'
        screenmanager.transition = CardTransition()
        screenmanager.transition.duration = .1

        self.sm = screenmanager

        #self.on_connected_change('','')

        return screenmanager

    def set_active_screen(self, screen):
        self.sm.current = screen

    def on_call_status_change(self, instance, value):
        Logger.info('App: Call Status callback is '+value+" ("+self.hfp.status+")")
        if value == "incoming":
            self.set_active_screen('telephony_incoming')
        if value == "active":
            self.set_active_screen('telephony_active')
        if value == "dialing":
            self.set_active_screen('telephony_dialling')
        if value == "disconnected":
            self.set_active_screen('music')

    def on_connected_change(self, instance, value):
        if self.a2dp.connected:
            self.set_active_screen('music')
        else:
            self.set_active_screen('homescreen')
