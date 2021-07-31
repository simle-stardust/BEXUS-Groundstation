import socket
import time
from datastructures.communicationdata import CommunicationData

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class CommunicationSignals(QObject):

    input_list = pyqtSignal(list)
    input_string = pyqtSignal(str)
    comms_data = pyqtSignal(CommunicationData)


class Communication(QRunnable):

    def __init__(self, udp_ip, udp_port, max_reps, mechanisms, state):
        super(Communication, self).__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((udp_ip, int(udp_port)))

        self.signals = CommunicationSignals()

        self.commsData = CommunicationData(pingerFlag=False,
                                           stateSwitchFlag=False,
                                           valveSwitchFlag=False,
                                           pumpSwitchFlag=False,
                                           pingOnce=False,
                                           pingInterval=0,
                                           stateToSet=0,
                                           valveId=0,
                                           valveStateToSet=0,
                                           pumpId=0,
                                           pumpStateToSet=0)

        self.pingRepetitions = 0
        self.stateSwitchRepetitions = 0
        self.valveSwitchRepetitions = 0
        self.pumpSwitchRepetitions = 0

        self.mechanisms = mechanisms
        self.experimentState = state

        self.lastPingTime = time.time()

        self.maxRepetitions = max_reps


    @pyqtSlot()
    def run(self):
        received_new = None
        received_last = None
        while True:
            received_new = self.socket.recvfrom(1024)
            received_to_list = list(str(received_new).split(","))
            self.signals.input_list.emit(received_to_list)
            self.signals.input_string.emit(received_new)

            if self.commsData.pingOnce:
                self.ping()
            if self.commsData.pingerFlag:
                self.pinger()

            if received_new != received_last:
                if self.commsData.stateSwitchFlag:
                    self.switchState(received_to_list[self.experimentState])
                if self.commsData.valveSwitchFlag:
                    self.switchValve(received_to_list[self.mechanisms['Valves']['status']])
                if self.commsData.pumpSwitchFlag:
                    self.switchState(received_to_list[self.mechanisms['Valves']['status']])
                self.signals.comms_data.emit(self.commsData)

            received_last = received_new

    def ping(self):
        self.socket.send(bytes("ping()"))
        self.commsData.pingOnce = False
    
    def pinger(self):
        if time.time() - self.lastPingTime >= self.commsData.pingInterval:
            self.socket.send(bytes("ping()"))
    
    def switchState(self, currentState):
        self.socket.send(bytes('setState(' + str(self.commsData.stateToSet) + ')'))
        if self.commsData.stateToSet != currentState or self.commsData.stateSwitchRepetitions <= self.maxRepetitions:
            self.commsData.stateSwitchFlag = False
            self.commsData.stateSwitchRepetitions = 0

    def switchValve(self, currentValveState):
        self.socket.send(bytes('setValve(' + str(self.commsData.valveId) + str(self.commsData.valveStateToSet) + ')'))
        if self.commsData.valveStateToSet != currentValveState or self.commsData.valveSwitchRepetitions <= self.maxRepetitions:
            self.commsData.valveSwitchFlag = False
            self.commsData.valveSwitchRepetitions = 0
    def switchPump(self, currentPumpState):
        self.socket.send(bytes('setPump(' + str(self.commsData.pumpId) + ', ' + str(self.commsData.pumpStateToSet) + ')'))
        if self.commsData.pumpStateToSet != currentPumpState or self.commsData.pumpSwitchRepetitions <= self.maxRepetitions:
            self.commsData.pumpSwitchFlag = False
            self.commsData.pumpSwitchRepetitions = 0
