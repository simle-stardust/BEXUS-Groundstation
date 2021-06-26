import socket

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class StateSignals(QObject):

    readings = pyqtSignal(list)


class StateSwitcher(QRunnable):

    def __init__(self, state, index):
        super(StateSwitcher, self).__init__()
        self.state = state
        self.index = index
        self.signals = StateSignals()

    @pyqtSlot()
    def run(self):
        while self.state != self.signals.readings[self.index]:
            print('setState(' + str(self.state) + ')')