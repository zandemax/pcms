import can
import threading


class CANBus(object):

    def __init__(self, ui):
        self.ui = ui
        self.bus = can.interface.Bus('infotainment', bustype='virtual')
        self.listener = can.BufferedReader()
        self.notifier = can.Notifier(self.bus, [self.listener])
        self.caniterator = CANIterator(self, self.listener)
        self.caniterator.start()

    def user_action(self, action):
        if action == 'up':
            self.ui.a2dp.previous()
        elif action == 'down':
            self.ui.a2dp.next()

    def on_stop(self):
        self.caniterator.stop()
        self.caniterator.join()
        self.notifier.stop()


class CANIterator(threading.Thread):

    def __init__(self, canbus, listener):
        threading.Thread.__init__(self)
        self.canbus = canbus
        self.listener = listener
        self.statuscodes = {bytes([0xC1, 0x0C]): 'up', bytes([0xC1, 0x00]): 'down'}
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while True:
            message = self.listener.get_message()
            if message is not None:
                self.eval_message(message)
            if self.stopped():
                break

    def eval_message(self, message):
        if message.arbitration_id == 0x1D6:
            data = bytes(message.data)
            if data in self.statuscodes:
                self.canbus.user_action(self.statuscodes[data])
