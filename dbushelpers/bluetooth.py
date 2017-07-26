from kivy.event import EventDispatcher
from kivy.properties import *
from kivy.logger import Logger
import pydbus


class BluetoothManager(EventDispatcher):

    connected = BooleanProperty()
    interfaces = DictProperty()
    modems = DictProperty()

    def __init__(self):
        bus = pydbus.SystemBus()
        self.bus = bus
        self.bluez = bus.get('org.bluez', '/')
        self.ofono = bus.get('org.ofono', '/')
        self.bluez.InterfacesAdded.connect(self.on_interfaces_added)
        self.bluez.InterfacesRemoved.connect(self.on_interfaces_removed)
        self.get_interfaces()
        #print(self.interfaces)
        self.get_modems()
        #print(self.modems)

    def get_interfaces(self):
        objects = self.bluez.GetManagedObjects()
        for object in objects:
            for interface in objects[object]:
                if 'org.bluez' in interface:
                    self.interfaces[interface] = object

    def get_modems(self):
        modems = self.ofono.GetModems()
        for modem in modems:
            self.modems[modem[0]] = modem[1]

    def on_interfaces_added(self, object, properties):
        #print(properties)
        #print(object)
        for i in properties:
            if 'org.bluez' in i:
                interface = i
        self.interfaces[interface] = object

    def on_interfaces_removed(self, object, properties):
        for i in properties:
            if 'org.bluez' in i:
                interface = i
        self.interfaces.pop(interface, None)
