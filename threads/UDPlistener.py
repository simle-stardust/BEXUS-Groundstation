import socket

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class UDPListenerSignals(QObject):

    list = pyqtSignal(list)
    string = pyqtSignal(str)


class UDPListener(QRunnable):

    def __init__(self, UDP_IP, UDP_PORT):
        super(UDPListener, self).__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((UDP_IP, UDP_PORT))

        self.signals = UDPListenerSignals()

    @pyqtSlot()
    def run(self):
        while True:
            #TODO stworzyć system rozpoznawania czy otrzymany pakiet zawiera dane do przedstawienia czy odpowiedź na zapytanie (z functions.py)
            self.signals.result.emit(self.socket.recvfrom(1024))
            #TODO zmienna list musi dostać listę wartości z socketa
