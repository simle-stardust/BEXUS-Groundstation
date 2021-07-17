import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class StateSwitcher(QRunnable):

    def __init__(self, expected, udp_ip, udp_port):
        super(StateSwitcher, self).__init__()
        self.stateToSet = expected
        self.currentState = None
        self.repetitions = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((udp_ip, udp_port))

    @pyqtSlot()
    def run(self):
        while self.stateToSet != self.currentState or self.repetitions <= 10:
            self.socket.send(bytes('setState(' + str(self.stateToSet) + ')'))
            print('setState(' + str(self.stateToSet) + ')')
            self.repetitions += 1
            time.sleep(1)
