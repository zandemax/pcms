from threading import Thread
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivy.support import install_gobject_iteration
from dbushelpers.a2dp import A2DPManager
from dbushelpers.telephony import TelephonyManager
from ui.components import *
from ui.components.homescreen import HomeScreen
from kivy.logger import Logger


class UserInterface(App):

    def build(self):
        install_gobject_iteration()

        self.telman = TelephonyManager()
        self.a2dp = A2DPManager(self.telman)
        self.a2dp.bind(connected=self.on_connected_change)

        self.telman.bind(status=self.on_call_status_change)


##### UI ######
        screenmanager = ScreenManager()
        #return TelephonyUI()
        self.musicplayer = MusicPlayer(name='music', a2dp=self.a2dp, app=self)
        screenmanager.add_widget(self.musicplayer)
        screenmanager.add_widget(TelephonyIncoming(name='telephony_incoming', telman=self.telman))
        screenmanager.add_widget(TelephonyDialling(name='telephony_dialling', telman=self.telman))
        screenmanager.add_widget(TelephonyActive(name='telephony_active', telman=self.telman))
        screenmanager.add_widget(Dialler(name='dialler', telman=self.telman, app=self))
        screenmanager.add_widget(HomeScreen(name='homescreen', app=self))
        screenmanager.current = 'homescreen'
        screenmanager.transition = CardTransition()
        screenmanager.transition.duration = .1

        self.sm = screenmanager

        #self.on_connected_change('','')

        return screenmanager

    def set_active_screen(self, screen):
        self.sm.current = screen

    def on_call_status_change(self, instance, value):
        Logger.info('App: Call Status callback is '+value+" ("+self.telman.status+")")
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
