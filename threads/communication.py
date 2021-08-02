import socket
from datetime import datetime
import time
from datastructures.communicationdata import CommunicationData

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


class CommunicationSignals(QObject):

    input_list = pyqtSignal(list)
    input_string = pyqtSignal(str)
    comms_data = pyqtSignal(CommunicationData)


class Communication(QRunnable):

    def __init__(self, ip_rx, port_rx, ip_tx, port_tx, max_reps, max_command_time, buffer_len, last_ping_time, mechanisms, state):
        super(Communication, self).__init__()

        self.sock_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('vvvvvvvvvvvvvv')
        print(ip_rx)
        print('- - - - - - -')
        print(port_rx)
        print('vvvvvvvvvvvvvv')
        self.sock_rx.bind((ip_rx, int(port_rx)))
        self.sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.ip_tx = ip_tx
        self.port_tx = port_tx

        self.bufferLenght = buffer_len
        self.lastPingTime = last_ping_time

        self.signals = CommunicationSignals()

        self.commsData = CommunicationData(pingerFlag=False,
                                           stateSwitchFlag=False,
                                           valveSwitchFlag=False,
                                           pumpSwitchFlag=False,
                                           pingOnce=False,
                                           isCommsOnline=False,
                                           pingInterval=0,
                                           stateToSet=0,
                                           valveId=0,
                                           valveStateToSet=0,
                                           pumpId=0,
                                           pumpStateToSet=0,
                                           stateSwitchStartedAt=0,
                                           valveSwitchStartedAt=0,
                                           pumpSwitchStartedAt=0)

        self.pingRepetitions = 0
        self.stateSwitchRepetitions = 0
        self.valveSwitchRepetitions = 0
        self.pumpSwitchRepetitions = 0

        self.maxCommandTime = max_command_time * 1000

        self.mechanisms = mechanisms
        self.experimentState = state

        self.lastPingTime = time.time()

        self.maxRepetitions = max_reps

        self.buffer = ""


    @pyqtSlot()
    def run(self):
        received_new_list = None
        received_last_list = None

        while True:
            received = self.sock_rx.recvfrom(1024)

            self.buffer = self.buffer + received[0].decode()
            #print(self.buffer)

            if "@" in self.buffer and ";" in self.buffer:

                received_new_list = list(self.buffer[self.buffer.find("@")+1 : self.buffer.find(";")].split(","))
                if len(received_new_list) == 1:
                    #error, flush the buffer up to "@"
                    self.buffer=self.buffer[self.buffer.find("@"):]
                else:
                    #print(received_new_list)
                    #print(len(received_new_list))
                    # only update data when all required fields are present
                    if len(received_new_list) == self.bufferLenght:
                        received_new_list = self.createList(received_new_list)
                        self.signals.input_list.emit(received_new_list)
                        self.signals.input_string.emit(self.buffer + "\r")
                    self.buffer=""

            if self.commsData.pingOnce:
                self.ping()
            if self.commsData.pingerFlag:
                self.pinger()

            if received_new_list != received_last_list and len(received_new_list) == self.bufferLenght:
                if self.commsData.stateSwitchFlag:
                    self.switchState(received_new_list[int(self.experimentState)])
                if self.commsData.valveSwitchFlag:
                    self.switchValve(received_new_list[int(self.mechanisms['Valves']['status'])])
                if self.commsData.pumpSwitchFlag:
                    self.switchState(received_new_list[int(self.mechanisms['Valves']['status'])])
                if int(received_new_list[int(self.lastPingTime)]) > 30:
                    self.commsData.isCommsOnline = False
                else:
                    self.commsData.isCommsOnline = True

                self.signals.comms_data.emit(self.commsData)

            received_last_list = received_new_list

    def ping(self):
        self.sock_tx.sendto(bytes("ping", encoding='utf8'), (self.ip_tx, self.port_tx))
        self.commsData.pingOnce = False
    
    def pinger(self):
        if time.time() - self.lastPingTime >= self.commsData.pingInterval:
            self.sock_tx.sendto(bytes("ping", encoding='utf8'), (self.ip_tx, self.port_tx))
    
    def switchState(self, currentState):
        self.sock_tx.sendto(bytes('setState_' + str(self.commsData.stateToSet), encoding='utf8'), (self.ip_tx, self.port_tx))
        if self.commsData.stateToSet != currentState or self.commsData.stateSwitchRepetitions <= self.maxRepetitions or time.time() - self.commsData.stateSwitchStartedAt > self.maxCommandTime:
            self.commsData.stateSwitchFlag = False
            self.commsData.stateSwitchRepetitions = 0

    def switchValve(self, currentValveState):
        self.sock_tx.sendto(bytes('setValve_' + str(self.commsData.valveId) + '_' + str(self.commsData.valveStateToSet), encoding='utf8'),
                           (self.ip_tx, self.port_tx))
        if self.commsData.valveStateToSet != currentValveState or self.commsData.valveSwitchRepetitions <= self.maxRepetitions or time.time() - self.commsData.valveSwitchStartedAt > self.maxCommandTime:
            self.commsData.valveSwitchFlag = False
            self.commsData.valveSwitchRepetitions = 0

    def switchPump(self, currentPumpState):
        self.sock_tx.sendto(bytes('setPump_' + str(self.commsData.pumpId) + '_' + str(self.commsData.pumpStateToSet), encoding='utf8'),
                           (self.ip_tx, self.port_tx))
        if self.commsData.pumpStateToSet != currentPumpState or self.commsData.pumpSwitchRepetitions <= self.maxRepetitions or time.time() - self.commsData.pumpSwitchStartedAt > self.maxCommandTime:
            self.commsData.pumpSwitchFlag = False
            self.commsData.pumpSwitchRepetitions = 0

    def createList(self, list_to_convert):
        for i in range (2, len(list_to_convert)):
            list_to_convert[i] = float(list_to_convert[i])

        date = list_to_convert[0].split('/')
        timestamp = list_to_convert[1].split('_')

        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        hour = int(timestamp[0])
        min = int(timestamp[1])
        sec = int(timestamp[2])

        dt = datetime(year, month, day, hour, min, sec)

        list_to_convert[0] = dt.timestamp()
        list_to_convert[1] = dt.timestamp()

        return list_to_convert