import socket
import time

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal

from threads.receivers import UDPlistener

class Communication(QObject):

    input_list = pyqtSignal(list)
    input_string = pyqtSignal(str)


class Communication(UDPlistener.UDPListener):

    def __init__(self, sock, interval):
        super(UDPlistener.UDPListener, self).__init__()

        self.socket = sock

        self.signals = UDPlistener.UDPListenerSignals()

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
        self.valveStateToSet = None
        self.currentValveState = None

        self.pumpId = None
        self.pumpStateToSet = None
        self.currenPumpState = None

        self.buffer = ""

    @pyqtSlot()
    def run(self):
        received_new = None
        received_last = None
        while True:
            received_new = self.socket.recvfrom(1024)
            self.buffer = self.buffer + received_new[0].decode()

            if "@" in self.buffer and ";" in self.buffer:

                received_new_list = list(self.buffer[self.buffer.find("@")+1 : self.buffer.find(";")].split(","))
                print(received_new_list)
                print(len(received_new_list))
                # only update data when all required fields are present
                if len(received_new_list) == 64:
                    self.signals.input_list.emit(received_new_list)
                    self.signals.input_string.emit(self.buffer)
                self.buffer=""

            if self.pingerFlag:
                self.ping()

            if received_new != received_last:
                if self.stateSwitchFlag:
                    self.switchState()
                if self.valveSwitchFlag:
                    self.switchValve()
                if self.pumpSwitchFlag:
                    self.switchPump()

            received_last = received_new

    
    def pinger(self):
        if time.time() - self.lastPingTime >= self.pingInterval:
            self.socket.send(bytes("ping", encoding='utf8'))
    
    def switchState(self):
        self.socket.send(bytes('setState_' + str(self.stateToSet), encoding='utf8'))
        if self.stateToSet != self.currentState or self.stateSwitchRepetitions <= self.maxRepetitions:
            self.stateSwitchFlag = False
            self.stateSwitchRepetitions = 0

    def switchValve(self):
        self.socket.send(bytes('setValve_' + str(self.valveId) + str(self.valveStateToSet)), encoding='utf8')
        if self.valveStateToSet != self.currentValveState or self.valveSwitchRepetitions <= self.maxRepetitions:
            self.valveSwitchFlag = False
            self.valveSwitchRepetitions = 0
            
    def switchPump(self):
        self.socket.send(bytes('setPump_' + str(self.pumpId) + '_' + str(self.pumpStateToSet)), encoding='utf8')
        if self.pumpStateToSet != self.currentPumpState or self.pumpSwitchRepetitions <= self.maxRepetitions:
            self.pumpSwitchFlag = False
            self.pumpSwitchRepetitions = 0
