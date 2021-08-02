import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class Pinger(QRunnable):

    def __init__(self, t, sock, ip_tx, port_tx):
        super(Pinger, self).__init__()
        self.interval = t
        self.ifPing = True

        self.socket = sock
        self.ip_tx = ip_tx
        self.port_tx = port_tx

    @pyqtSlot()
    def run(self):
        while self.ifPing:
            self.socket.sendto(bytes("ping", encoding='utf8'), (self.ip_tx, self.port_tx))
            print("ping")
            time.sleep(float(self.interval))
