import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class Pinger(QRunnable):

    def __init__(self, t, sock):
        super(Pinger, self).__init__()
        self.interval = t
        self.ifPing = True

        self.socket = sock

    @pyqtSlot()
    def run(self):
        while self.ifPing:
            self.socket.send(bytes("ping()"))
            print("ping()")
            time.sleep(float(self.interval))
