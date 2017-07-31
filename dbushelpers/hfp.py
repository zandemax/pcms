from kivy.event import EventDispatcher
from kivy.properties import (StringProperty, NumericProperty,
                             ObjectProperty, BooleanProperty)
from kivy.logger import Logger


class HFPManager(EventDispatcher):

    connected = BooleanProperty()
    status = StringProperty()
    carrier = StringProperty()
    network_strength = NumericProperty()
    active_call = ObjectProperty()
    held_call = ObjectProperty()
    pending_call = ObjectProperty()

    def __init__(self, bluetooth):
        Logger.info('Telephony: Loading telephony-module ...')
        bluetooth.bind(modems=self.on_modems_change)
        self.bluetooth = bluetooth
        self.on_modems_change(self, bluetooth.modems)

    def on_modems_change(self, instance, value):
        for modem in value:
            if value[modem]['Online'] is True:
                self.modem = self.bluetooth.bus.get('org.ofono', modem)
                self.modem.CallAdded.connect(self.on_call_added)
                self.modem[
                    'org.ofono.NetworkRegistration'].PropertyChanged.connect(
                        self.on_netstat_changed)
                self.connected = True
                Logger.info('HFP: Connected')
                self.get_properties()
                return
        self.modem = None
        self.connected = False

    def call(self, number):
        self.modem.Dial(number, '')
        self.status = "dialling"
        Logger.info('Telephony: Call initialised')

    def end_call(self, call):
        call.Hangup()

    def on_property_changed(self, sender, message):
        Logger.info('Telephony: '+sender+' changed to '+message)
        if sender == 'State':
            self.status = message
        elif sender == 'Name':
            self.network_name = message

    def on_netstat_changed(self, sender, message):
        Logger.info('Network: '+sender+' '+str(message))
        if sender == 'Name':
            self.carrier = message
        elif sender == 'Strength':
            self.network_strength = message

    def accept_call(self):
        self.active_call['call'].Accept()

    def on_call_added(self, sender, message):
        self.active_call = {'call': self.bus.get(
            'org.ofono', sender), 'properties': message}
        self.active_call['call'].PropertyChanged.connect(
            self.on_property_changed)
        self.status = message['State']

    def get_properties(self):
        properties = self.modem[
            'org.ofono.NetworkRegistration'].GetProperties()
        Logger.info('Network: '+str(properties))
        try:
            self.carrier = properties['Name']
            self.network_strength = properties['Strength']
        except KeyError:
            pass
