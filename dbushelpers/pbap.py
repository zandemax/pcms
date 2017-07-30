from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from gi.repository import GLib
import pydbus
import vobject

class PhonebookManager(EventDispatcher):

    loaded = BooleanProperty(False)

    def __init__(self, bluetooth):
        self.bus = pydbus.SessionBus()
        self.obex = self.bus.get('org.bluez.obex', '/org/bluez/obex')
        bluetooth.bind(modems = self.get_phonebook)
        self.bluetooth = bluetooth
        self.transfer = None
        self.get_phonebook()
        self.phonebook = []

    def connect(self):
        print('connecting')
        print(self.bluetooth.get_device_serial())
        #session_path = self.obex.CreateSession(self.bluetooth.get_device_serial(), {"Target":GLib.Variant('s','PBAP')})
        session_path = self.obex.CreateSession('DC:D9:16:32:CA:AB',{ "Target": GLib.Variant('s','PBAP') })
        session = self.bus.get('org.bluez.obex', session_path)
        return session

    def get_phonebook(self):
        print('loading pb')
        session = self.connect()
        session.Select('int', 'pb')
        transfer_path, transfer_args = session.PullAll('',{ "Format" : GLib.Variant('s','vcard30') })
        print(transfer_path)
        self.transfer = self.bus.get('org.bluez.obex', transfer_path)
        self.transfer.PropertiesChanged.connect(self.on_property_changed)
        self.pb_filename = transfer_args['Filename']
        print(self.pb_filename)

    def on_property_changed(self, property, value, c):
        try:
            if value['Status'] == 'complete':
                self.read_vcard_file(self.pb_filename, self.phonebook)
                self.loaded = True
        except KeyError:
            pass

    def read_vcard_file(self, filename, list):
        print('loading cards')
        cards_file = open(filename,'r')
        vcard = ''
        for line in cards_file:
            if 'END:VCARD' in line:
                vcard = vcard + line
                self.process_vcard(vcard, list)
                vcard = ''
            else:
                vcard = vcard + line

    def process_vcard(self, vcard, list):
        vcard_obj = vobject.readOne(vcard)
        list.append(vcard_obj)
