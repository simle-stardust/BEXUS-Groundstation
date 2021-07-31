import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class PumpSwitcher(QRunnable):

    def __init__(self, index, expected, sock, ip_tx, port_tx):
        super(PumpSwitcher, self).__init__()
        self.pumpId = index
        self.pumpStateToSet = expected
        self.currentPumpState = None
        self.repetitions = 0

        self.socket = sock
        self.ip_tx = ip_tx
        self.port_tx = port_tx

    @pyqtSlot()
    def run(self):
        while self.pumpStateToSet != self.currentPumpState and self.repetitions <= 10:
            self.socket.sendto(bytes('setPump_' + str(self.pumpId) + '_' + str(self.pumpStateToSet), encoding='utf8'), (self.ip_tx, self.port_tx))
            print('setPump_' + str(self.pumpId) + "_" + str(self.pumpStateToSet))
            self.repetitions += 1
            time.sleep(1)
