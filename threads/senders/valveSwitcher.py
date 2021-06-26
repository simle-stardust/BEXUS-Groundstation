import socket

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class ValveSignals(QObject):

    readings = pyqtSignal(list)


class ValveSwitcher(QRunnable):

    def __init__(self, valveId, valveState, index):
        super(ValveSwitcher, self).__init__()
        self.valveId = valveId
        self.valveState = valveState
        self.index = index
        self.signals = ValveSignals()

    @pyqtSlot()
    def run(self):
        while self.valveState != self.signals.readings[self.index]:
            print('setPump(' + str(self.valveId) + str(self.valveState) + ')')