from kivy.app import App
#from kivy.uix.screenmanager import CardTransition
from kivy.support import install_gobject_iteration
from dbushelpers import (A2DPManager, HFPManager,
                         PhonebookManager, BluetoothManager)
from canhelpers.canbus import CANBus
from ui.components import BaseView
from ui.components.screen import (MusicScreen, HomeScreen,
                                  ContactScreen, PhoneScreen, SettingsScreen)
from kivy.logger import Logger


class UserInterface(App):

    def build(self):
        install_gobject_iteration()

        self.bluetooth = BluetoothManager()
        self.hfp = HFPManager(self.bluetooth)
        self.a2dp = A2DPManager(self.bluetooth)
        self.pbap = PhonebookManager(self.bluetooth, self.hfp)
        self.canbus = CANBus(self)
        self.a2dp.bind(connected=self.on_connected_change)
        #self.hfp.bind(status=self.on_call_status_change)
        self.hfp.bind(attention=self.on_hfp_attention_change)

        view = BaseView()

        self.statusbar = view.ids.statusbar
        self.statusbar.set_app(self)
        self.statusbar.set_title('Home')
        self.controlbar = view.ids.controlbar
        self.controlbar.ids.phone.bind(on_press=self.on_screen_switch)
        self.controlbar.ids.home.bind(on_press=self.on_screen_switch)
        self.controlbar.ids.music.bind(on_press=self.on_screen_switch)
        self.controlbar.ids.settings.bind(on_press=self.on_screen_switch)

        screenmanager = view.ids.screenmanager
        screenmanager.add_widget(MusicScreen(name='musicscreen',
                                             a2dp=self.a2dp,
                                             app=self))
        screenmanager.add_widget(ContactScreen(name='contactscreen',
                                               pbap=self.pbap, hfp=self.hfp))
        screenmanager.add_widget(HomeScreen(name='homescreen',
                                            app=self))
        screenmanager.add_widget(PhoneScreen(name='phonescreen',
                                             hfp=self.hfp, pbap=self.pbap))
        screenmanager.add_widget(SettingsScreen(name='settingsscreen'))
        screenmanager.current = 'settingsscreen'
#        screenmanager.transition = CardTransition()
        screenmanager.transition.duration = .1
        self.sm = screenmanager
        self.screen_names = {'musicscreen': 'Music',
                             'contactscreen': 'Phone',
                             'homescreen': 'Home',
                             'phonescreen': 'Call',
                             'settingsscreen': 'Settings'}
#        self.on_connected_change(self, self.a2dp.connected)
        self.previous_screen = 'homescreen'
        return view

    def on_screen_switch(self, instance):
        if instance == self.controlbar.ids.phone:
            self.sm.transition.direction = 'right'
            self.set_active_screen('contactscreen')
        if instance == self.controlbar.ids.home:
            if self.sm.transition.direction == 'right':
                self.sm.transition.direction = 'left'
            else:
                self.sm.transition.direction = 'right'
            self.set_active_screen('homescreen')
        if instance == self.controlbar.ids.music:
            self.sm.transition.direction = 'left'
            self.set_active_screen('musicscreen')
        if instance == self.controlbar.ids.settings:
            self.sm.transition.direction = 'left'
            self.set_active_screen('settingsscreen')

    def set_active_screen(self, screen):
        self.statusbar.set_title(self.screen_names[screen])
        self.controlbar.set_active_icon(screen)
        self.sm.current = screen

    def on_hfp_attention_change(self, instance, value):
        if value[0] is not None:
            if self.sm.current != 'phonescreen':
                self.previous_screen = self.sm.current
            self.set_active_screen('phonescreen')
        else: self.set_active_screen(self.previous_screen)

    def on_connected_change(self, instance, value):
        if value is True:
            self.set_active_screen('musicscreen')
        else:
            self.set_active_screen('homescreen')

    def on_stop(self):
        self.canbus.on_stop()
