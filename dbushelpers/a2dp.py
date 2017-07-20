import pydbus
from kivy.event import EventDispatcher
from kivy.properties import *
from kivy.logger import Logger


class A2DPManager(EventDispatcher):

    connected = BooleanProperty(False)
    status = StringProperty('paused')
    title = StringProperty()
    artist = StringProperty()
    duration = NumericProperty()
    current_pos = NumericProperty()

    def __init__(self, telman):
        super().__init__()
        Logger.info('A2DP: Loading a2dp-module')
        self.bus = pydbus.SystemBus()
        self.gui = None
        self.bluez = self.bus.get('org.bluez','/org/bluez/hci0')
        self.bluez_base = self.bus.get('org.bluez','/')
        self.telman = telman
        try:
            self.player = self.get_player()
            self.connected = True
            self.player.PropertiesChanged.connect(self.signal_callback)
            Logger.info('A2DP: Connected')
        except AttributeError:
            self.connected = False

        self.bluez_base.InterfacesAdded.connect(self.check_player_new)
        self.bluez_base.InterfacesRemoved.connect(self.check_player_removed)
    #    self.player = self.bus.get('org.bluez','/org/bluez/hci0/dev_DC_D9_16_32_CA_AB/player0')
    #    self.player = self.bus.get('org.bluez','/org/bluez/hci0/dev_84_51_81_B4_9D_0F/player0')

    def get_player(self):
        managed_objects = self.bluez_base.GetManagedObjects()
        object_string = None

        for i in managed_objects:
#            print(i)
            device = 'org.bluez.Device1' in managed_objects[i]
#            print(device)
            if device:
#                print('found')
                if managed_objects[i]['org.bluez.Device1']['Connected'] == True:
                    object_string = i
                    Logger.info('Bluetooth: Device connected')

        if object_string is None:
            raise AttributeError('could not get connected device')
            return
        device = self.bus.get('org.bluez',object_string)
        Logger.info('A2DP: Trying to connect HFP')
        self.telman.connect(object_string)
        player = self.bus.get('org.bluez', object_string+'/player0')
        message = player.GetAll('org.bluez.MediaPlayer1')
        track = message['Track']
        self.title = track['Title']
        self.artist = track['Artist']
        self.duration = track['Duration']
        self.status = message['Status']
        self.current_pos = message['Position']
        return player


    def check_player_new(self, sender, message):
        if 'org.bluez.MediaPlayer1' in message:
            device_string = message['org.bluez.MediaPlayer1']['Device']
            self.telman.connect(device_string)
            self.player = self.bus.get('org.bluez', device_string+'/player0')
            self.connected = True

    def check_player_removed(self, sender, message):
        if 'org.bluez.MediaPlayer1' in message:
            self.connected = False
            self. player = None

    def update_player_data(self):
        message = self.player.GetAll('org.bluez.MediaPlayer1')
        track = message['Track']
        self.title = track['Title']
        self.artist = track['Artist']
        self.duration = track['Duration']
        self.status = message['Status']
        self.current_pos = message['Position']

    def signal_callback(self, sender, message, c):
        if 'Track' in message:
            print('track')
            track = message['Track']
            labels = {'title':track['Title'], 'artist':track['Artist'], 'duration':track['Duration']}
            self.title = labels['title']
            self.artist = labels['artist']
            self.duration = labels['duration']
        elif 'Status' in message:
            print('status')
            self.status = message['Status']
            print(self.status)
        elif 'Position' in message:
            print('position')
            self.current_pos = message['Position']


    def set_gui(self, gui):
        self.gui = gui

    def pause(self):
        if self.connected:
            self.player.Pause()

    def play(self):
        if self.connected:
            self.player.Play()

    def next(self):
        if self.connected:
            self.player.Next()

    def previous(self):
        if self.connected:
            self.player.Previous()
