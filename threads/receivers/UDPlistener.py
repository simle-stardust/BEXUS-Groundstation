import socket

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class UDPListenerSignals(QObject):

    input_list = pyqtSignal(list)
    input_string = pyqtSignal(str)


class UDPListener(QRunnable):

    def __init__(self, sock):
        super(UDPListener, self).__init__()

        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket = sock

        self.signals = UDPListenerSignals()

    @pyqtSlot()
    def run(self):
        while True:
            received_temp = self.socket.recvfrom(1024)
            self.signals.input_list.emit(list(received_temp.split(",")))
            self.signals.input_string.emit(received_temp)