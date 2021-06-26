import socket

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class PingSignals(QObject):

    ifPing = pyqtSignal(bool)


class Pinger(QRunnable):

    def __init__(self):
        super(Pinger, self).__init__()

        self.signals = PingSignals()

    @pyqtSlot()
    def run(self):
        while self.signals.ifPing():
            print('setPump(ping)')