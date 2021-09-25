import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class ValveSwitcher(QRunnable):

    def __init__(self, index, expected, sock, ip_tx, port_tx):
        super(ValveSwitcher, self).__init__()
        self.valveId = index
        self.valveStateToSet = expected
        self.currentValveState = None
        self.repetitions = 0

        self.socket = sock
        self.ip_tx = ip_tx
        self.port_tx = port_tx

    @pyqtSlot()
    def run(self):
        while self.valveStateToSet != self.currentValveState and self.repetitions <= 1:
            self.socket.sendto(bytes('setValve_' + str(self.valveId) + '_' + str(self.valveStateToSet), encoding='utf8'), (self.ip_tx, self.port_tx))
            print('setValve_' + str(self.valveId) + '_' + str(self.valveStateToSet))
            self.repetitions += 1
            time.sleep(1)
