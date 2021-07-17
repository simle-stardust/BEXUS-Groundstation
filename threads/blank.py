import time
from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class BlankSignals(QObject):

    result = pyqtSignal(list)


class Blank(QRunnable):

    def __init__(self):
        super(Blank, self).__init__()

        self.signals = BlankSignals()

        self.index = 0

    @pyqtSlot()
    def run(self):
        while self.index < 10:
            self.index += 1
            print("blank")
            time.sleep(0.6)
