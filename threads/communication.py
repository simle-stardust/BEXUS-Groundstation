import socket
import time

from datetime import datetime

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal

from threads.receivers import UDPlistener

class Communication(QObject):

    input_list = pyqtSignal(list)
    input_string = pyqtSignal(str)


class Communication(UDPlistener.UDPListener):

    def __init__(self, sock_rx, sock_tx, ip_tx, port_tx, interval):
        super(UDPlistener.UDPListener, self).__init__()

        self.sock_rx = sock_rx
        self.sock_tx = sock_tx
        self.ip_tx = ip_tx 
        self.port_tx = port_tx

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
            received_new = self.sock_rx.recvfrom(1024)
            self.buffer = self.buffer + received_new[0].decode()

            print(self.buffer)

            if "@" in self.buffer and ";" in self.buffer:

                received_new_list = list(self.buffer[self.buffer.find("@")+1 : self.buffer.find(";")].split(","))
                print(received_new_list)
                print(len(received_new_list))
                # only update data when all required fields are present
                if len(received_new_list) == 65:
                    self.signals.input_list.emit(self.createList(received_new_list))
                    self.signals.input_string.emit(self.buffer + "\r")
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
            self.sock_tx.sendto(bytes("ping", encoding='utf8'))
    
    def switchState(self):
        self.sock_tx.sendto(bytes('setState_' + str(self.stateToSet), encoding='utf8'), (self.ip_tx, self.port_tx))
        if self.stateToSet != self.currentState or self.stateSwitchRepetitions <= self.maxRepetitions:
            self.stateSwitchFlag = False
            self.stateSwitchRepetitions = 0

    def switchValve(self):
        self.sock_tx.sendto(bytes('setValve_' + str(self.valveId) + str(self.valveStateToSet), encoding='utf8'), (self.ip_tx, self.port_tx))
        if self.valveStateToSet != self.currentValveState or self.valveSwitchRepetitions <= self.maxRepetitions:
            self.valveSwitchFlag = False
            self.valveSwitchRepetitions = 0
            
    def switchPump(self):
        self.sock_tx.sendto(bytes('setPump_' + str(self.pumpId) + '_' + str(self.pumpStateToSet), encoding='utf8'), (self.ip_tx, self.port_tx))
        if self.pumpStateToSet != self.currentPumpState or self.pumpSwitchRepetitions <= self.maxRepetitions:
            self.pumpSwitchFlag = False
            self.pumpSwitchRepetitions = 0

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