import pydbus
from gi.repository import GLib
from kivy.event import EventDispatcher
from kivy.properties import *
from kivy.logger import Logger

class TelephonyManager(EventDispatcher):

    status = StringProperty()
    carrier = StringProperty()
    network_strength = NumericProperty()
    active_call = ObjectProperty()
    held_call = ObjectProperty()
    pending_call = ObjectProperty()

    def __init__(self):
        Logger.info('Telephony: Loading telephony-module ...')
        self.bus = pydbus.SystemBus()
        self.ofono = self.bus.get('org.ofono','/')
        self.connected = False

    def connect(self, path):
        modems = self.ofono.GetModems()
        for i in modems:
            if '/hfp'+path in i:
                modem = self.bus.get('org.ofono','/hfp'+path)
                modem.SetProperty('Powered', GLib.Variant('b', True))
                self.connected = True
                self.modem = modem
                self.modem.CallAdded.connect(self.on_call_added)
                print(self.modem['org.ofono.NetworkRegistration'].PropertyChanged.connect(self.on_netstat_changed))
                self.get_properties()
                Logger.info('Telephony: Connected HFP device')

    def call(self, number):
        #self.number = number
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
        self.active_call = {'call':self.bus.get('org.ofono',sender),'properties':message}
        self.active_call['call'].PropertyChanged.connect(self.on_property_changed)
        self.status = message['State']

    def get_properties(self):
        properties = self.modem['org.ofono.NetworkRegistration'].GetProperties()
        Logger.info('Network: '+str(properties))
        self.carrier = properties['Name']
        self.network_strength = properties['Strength']
