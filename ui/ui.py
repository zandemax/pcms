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

        view = BaseView()

        self.statusbar = view.ids.statusbar
        self.statusbar.set_app(self)
        self.statusbar.set_title('Home')
        self.controlbar = view.ids.controlbar
        self.controlbar.ids.phone.bind(on_press=self.on_screen_switch)
        self.controlbar.ids.home.bind(on_press=self.on_screen_switch)
        self.controlbar.ids.music.bind(on_press=self.on_screen_switch)


        screenmanager = view.ids.screenmanager
        screenmanager.add_widget(MusicPlayer(name='music', a2dp=self.a2dp, app=self))
        screenmanager.add_widget(Phonebook(name='phonebook', pbap=self.pbap))
        screenmanager.add_widget(HomeScreen(name='homescreen', app=self))
        screenmanager.current = 'homescreen'
        screenmanager.transition = CardTransition()
        screenmanager.transition.duration = .1
        self.sm = screenmanager
        self.screen_names = {'music': 'Music', 'phonebook': 'Phone', 'homescreen': 'Home'}
        self.on_connected_change('','')
        return view

    def on_screen_switch(self, instance):
        if instance == self.controlbar.ids.phone:
            self.set_active_screen('phonebook')
        if instance == self.controlbar.ids.home:
            self.set_active_screen('homescreen')
        if instance == self.controlbar.ids.music:
            self.set_active_screen('music')

    def set_active_screen(self, screen):
        self.statusbar.set_title(self.screen_names[screen])
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
