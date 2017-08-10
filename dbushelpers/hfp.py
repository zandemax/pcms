from kivy.event import EventDispatcher
from kivy.properties import (StringProperty, NumericProperty,
                             ListProperty, BooleanProperty, ObjectProperty)
from kivy.logger import Logger


class HFPManager(EventDispatcher):

    connected = BooleanProperty()
    status = StringProperty()
    carrier = StringProperty()
    network_strength = NumericProperty()
    calls = ListProperty()
    attention = ListProperty()

    def __init__(self, bluetooth):
        Logger.info('HFP: Loading hfp-module')
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
        Logger.info('HFP: Call initialised')

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

    def accept_call(self, call):
        call.Accept()

    def on_call_added(self, path, properties):
        call = Call(path, self.bluetooth, properties, self)
        self.calls.append(call)
        Logger.info('HFP: Call created')

    def on_call_removed(self, path, properties):
        for call in self.calls:
            if call.path == path:
                self.calls.pop(call)
        Logger.info('HFP: Call destroyed')

    def get_properties(self):
        properties = self.modem[
            'org.ofono.NetworkRegistration'].GetProperties()
        Logger.info('Network: '+str(properties))
        try:
            self.carrier = properties['Name']
            self.network_strength = properties['Strength']
        except KeyError:
            pass


class Call(EventDispatcher):

    status = StringProperty()
    line_id = StringProperty()

    def __init__(self, path, bluetooth, properties, hfp):
        self.path = path
        self.hfp = hfp
        self.object = bluetooth.bus.get('org.ofono', path)
        self.object.PropertyChanged.connect(self.on_property_changed)
        self.status = properties['State']
        self.line_id = properties['LineIdentification']
        self.on_property_changed('State', self.status)

    def on_property_changed(self, property, value):
        Logger.info('Call: '+property+' changed to '+value)
        if property == 'State':
            self.state = value
            if (self.state != 'held' or self.state != 'disconnected'):
                self.hfp.attention = [self, self.state]
                Logger.info('Call: Attention aquired')
            if (self.state == 'held' or self.state == 'disconnected'):
                self.hfp.attention = [None, None]
                Logger.info('Call: Attention realeased')
