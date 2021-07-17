import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class Communication(QObject):

    input_list = pyqtSignal(list)
    input_string = pyqtSignal(str)


class Communication(QRunnable):

    def __init__(self, udp_ip, udp_port, interval):
        super(UDPListener, self).__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((udp_ip, int(udp_port)))

        self.signals = UDPListenerSignals()

        self.pingerFlag = False
        self.stateSwitchFlag = False
        self.valveSwitchFlag = False
        self.pumpSwitchFlag = False

        self.pingInterval = interval
        self.lastPingTime = time.time()

        self.pingRepetitions = 0
        self.stateSwitchRepetitions = 0
        self.valveSwitchRepetitions = 0
        self.pumpSwitchRepetitions = 0

        self.maxRepetitions = 10

        self.stateToSet = None
        self.currentState = None

        self.valveId = None
        self valveStateToSet = None
        self.currentValveState = None

        self.pumpId = None
        self pumpStateToSet = None
        self.currenPumpState = None



    @pyqtSlot()
    def run(self):
        received_new = None
        received_last = None
        while True:
            received_new = self.socket.recvfrom(1024)
            print(received_new)
            self.signals.input_list.emit(list(received_new.split(",")))
            self.signals.input_string.emit(received_new)

            if self.pingerFlag:
                self.ping()

            if received_new != received_last
                if self.stateSwitchFlag:
                    self.switchState()
                if self.valveSwitchFlag:
                    self.switchValve()
                if self.pumpSwitchFlag:
                    self.switchState()

            received_last = received_new

    
    def pinger():
        if time.time() - self.lastPingTime >= self.pingInterval:
            self.socket.send(bytes("ping()"))
    
    def switchState():
        self.socket.send(bytes('setState(' + str(self.stateToSet) + ')'))
        if self.stateToSet != self.currentState or self.stateSwitchRepetitions <= self.maxRepetitions:
            self.stateSwitchFlag = False
            self.stateSwitchRepetitions = 0

    def switchValve():
        self.socket.send(bytes('setValve(' + str(self.valveId) + str(self.valveStateToSet) + ')'))
        if self.valveStateToSet != self.currentValveState or self.valveSwitchRepetitions <= self.maxRepetitions
            self.valveSwitchFlag = False
            self.valveSwitchRepetitions = 0
    def switchPump()
        self.socket.send(bytes('setPump(' + str(self.pumpId) + ', ' + str(self.pumpStateToSet) + ')'))
        if self.pumpStateToSet != self.currentPumpState or self.pumpSwitchRepetitions <= self.maxRepetitions:
            self.pumpSwitchFlag = False
            self.pumpSwitchRepetitions = 0
