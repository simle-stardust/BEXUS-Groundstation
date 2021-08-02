import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class PumpSwitcher(QRunnable):

    def __init__(self, index, expected, sock):
        super(PumpSwitcher, self).__init__()
        self.pumpId = index
        self.pumpStateToSet = expected
        self.currentPumpState = None
        self.repetitions = 0

        self.socket = sock

    @pyqtSlot()
    def run(self):
        while self.pumpStateToSet != self.currentPumpState or self.repetitions <= 10:
            self.socket.send(bytes('setPump(' + str(self.pumpId) + ', ' + str(self.pumpStateToSet) + ')'))
            print('setPump(' + str(self.pumpId) + str(self.pumpStateToSet) + ')')
            self.repetitions += 1
            time.sleep(1)
