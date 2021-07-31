import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class StateSwitcher(QRunnable):

    def __init__(self, expected, sock, ip_tx, port_tx):
        super(StateSwitcher, self).__init__()
        self.stateToSet = expected
        self.currentState = None
        self.repetitions = 0

        self.socket = sock
        self.ip_tx = ip_tx
        self.port_tx = port_tx

    @pyqtSlot()
    def run(self):
        while self.stateToSet != self.currentState and self.repetitions <= 10:
            self.socket.sendto(bytes('setState_' + str(self.stateToSet), encoding='utf8'), (self.ip_tx, self.port_tx))
            print('setState_' + str(self.stateToSet))
            self.repetitions += 1
            time.sleep(1)
