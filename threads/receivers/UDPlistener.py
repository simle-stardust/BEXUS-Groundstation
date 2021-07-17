import socket

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class UDPListenerSignals(QObject):

    list = pyqtSignal(list)
    string = pyqtSignal(str)


class UDPListener(QRunnable):

    def __init__(self, udp_ip, udp_port):
        super(UDPListener, self).__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((udp_ip, udp_port))

        self.signals = UDPListenerSignals()

    @pyqtSlot()
    def run(self):
        while True:
            self.signals.result.emit(self.socket.recvfrom(1024))
            #TODO zmienna list musi dostać listę wartości z socketa