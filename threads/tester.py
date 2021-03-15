import time
import random

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class TesterSignals(QObject):


    result = pyqtSignal(list)



class Tester(QRunnable):

    def __init__(self, testingObject):
        super(Tester, self).__init__()
        self.testingObject = testingObject

        self.signals = TesterSignals()

        self.tim = 1
        self.high = 0

    @pyqtSlot()
    def run(self):
        while True:
            self.tim += 1
            self.high += random.randint(2, 6)
            self.testDataRandom = [0, self.tim, random.randint(300, 400) / 10, random.randint(0, 4), 0,0, 0, 0, self.high, 0, 0, random.randint(60,80), random.randint(67,73), 0, random.randint(60,80), random.randint(67,73), 0, random.randint(10000,100100)/10, random.randint(50000,70100)/10, random.randint(300,400)/10, 0,random.randint(10000,100100)/10, random.randint(50000,70100)/10, random.randint(300,400)/10, 0, random.randint(30,70), random.randint(400,500)/10, random.randint(30,70), random.randint(600,700)/10, 0,0,0,0,0 ]
            self.signals.result.emit(self.testDataRandom)
            time.sleep(0.1)