from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from kivy.logger import Logger
from gi.repository import GLib
import pydbus
import vobject


class PhonebookManager(EventDispatcher):

    loaded = BooleanProperty(False)

    def __init__(self, bluetooth, hfp):
        self.bus = pydbus.SessionBus()
        self.obex = self.bus.get('org.bluez.obex', '/org/bluez/obex')
        self.bluetooth = bluetooth
        self.transfer = None
        self.phonebook = []
        self.callhistory = []
        hfp.bind(connected=self.on_connected_change)
        self.on_connected_change(self, hfp.connected)
#        self.get_phonebook()

    def on_connected_change(self, instance, value):
        if value is True:
            self.get_phonebook()

    def connect(self):
        Logger.info('PBAP: Connecting')
        print(self.bluetooth.get_device_serial())
        session_path = self.obex.CreateSession(
            self.bluetooth.get_device_serial(),
            {"Target": GLib.Variant('s', 'PBAP')})
        session = self.bus.get('org.bluez.obex', session_path)
        return session

    def get_phonebook(self):
        Logger.info('PBAP: Loading phonebook')
        session = self.connect()
        session.Select('int', 'pb')
        transfer_path, transfer_args = session.PullAll('', {"Format": GLib.Variant('s', 'vcard30')})
        print(transfer_path)
        self.transfer = self.bus.get('org.bluez.obex', transfer_path)
        self.transfer.PropertiesChanged.connect(self.on_property_pb_changed)
        self.pb_filename = transfer_args['Filename']
        print(self.pb_filename)

    def get_calllist(self):
        Logger.info('PBAP: Loading calls')
        session = self.connect()
        session.Select('int', 'cch')
        transfer_path, transfer_args = session.PullAll('', {"Format": GLib.Variant('s', 'vcard30')})
        print(transfer_path)
        self.transfer = self.bus.get('org.bluez.obex', transfer_path)
        self.transfer.PropertiesChanged.connect(self.on_property_cch_changed)
        self.cch_filename = transfer_args['Filename']
        print(self.cch_filename)

    def on_property_pb_changed(self, property, value, c):
        try:
            if value['Status'] == 'complete':
                self.read_vcard_file(self.pb_filename, self.phonebook)
                self.loaded = True
        except KeyError:
            pass

    def on_property_cch_changed(self, property, value, c):
        try:
            if value['Status'] == 'complete':
                self.read_vcard_file(self.cch_filename, self.callhistory)
                self.loaded = True
        except KeyError:
            pass

    def read_vcard_file(self, filename, list):
        Logger.info('PBAP: Loading cards')
        cards_file = open(filename, 'r')
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
        try:
            for i in vcard_obj.x_group_membership_list:  # If contanct is in Group 'SD', add to our contactlist
                if i.value == 'SD':
                    list.append(vcard_obj)
        except (AttributeError, KeyError):
            pass  # Contact has no Group membership, continue

    def phonebook_search(self, number):
        raise KeyError
