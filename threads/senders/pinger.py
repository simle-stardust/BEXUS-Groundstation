import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot


class Pinger(QRunnable):

    def __init__(self, t, udp_ip, udp_port):
        super(Pinger, self).__init__()
        self.interval = t
        self.ifPing = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((udp_ip, udp_port))

    @pyqtSlot()
    def run(self):
        while self.ifPing:
            self.socket.send(bytes("ping()"))
            print("ping()")
            time.sleep(float(self.interval))
