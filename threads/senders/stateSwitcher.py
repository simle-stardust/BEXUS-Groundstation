import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class StateSwitcher(QRunnable):

    def __init__(self, expected, sock):
        super(StateSwitcher, self).__init__()
        self.stateToSet = expected
        self.currentState = None
        self.repetitions = 0

        self.socket = sock

    @pyqtSlot()
    def run(self):
        while self.stateToSet != self.currentState or self.repetitions <= 10:
            self.socket.send(bytes('setState(' + str(self.stateToSet) + ')'))
            print('setState(' + str(self.stateToSet) + ')')
            self.repetitions += 1
            time.sleep(1)
