import socket

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class PumpSignals(QObject):

    readings = pyqtSignal(list)


class PumpSwitcher(QRunnable):

    def __init__(self, pumpId, pumpState, index):
        super(PumpSwitcher, self).__init__()
        self.pumpId = pumpId
        self.pumpState = pumpState
        self.index = index
        self.signals = PumpSignals()

    @pyqtSlot()
    def run(self):
        while self.pumpState != self.signals.readings[self.index]:
            print('setPump(' + str(self.pumpId) + str(self.pumpState) + ')')