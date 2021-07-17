import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class ValveSwitcher(QRunnable):

    def __init__(self, index, expected, sock):
        super(ValveSwitcher, self).__init__()
        self.valveId = index
        self.valveStateToSet = expected
        self.currentValveState = None
        self.repetitions = 0

        self.socket = sock

    @pyqtSlot()
    def run(self):
        while self.valveStateToSet != self.currentValveState or self.repetitions <= 10:
            self.socket.send(bytes('setPump(' + str(self.valveId) + str(self.valveStateToSet) + ')'))
            print('setPump(' + str(self.valveId) + str(self.valveStateToSet) + ')')
            self.repetitions += 1
            time.sleep(1)
