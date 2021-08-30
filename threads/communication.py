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

    def __init__(self, ip_rx, port_rx, ip_tx, port_tx, max_reps, max_command_time, buffer_len, last_confirmation_id,
                 mechanisms, state):
        super(Communication, self).__init__()

        self.sock_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_rx.bind((ip_rx, int(port_rx)))
        self.sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.ip_tx = ip_tx
        self.port_tx = port_tx

        self.bufferLength = buffer_len
        self.lastConnectionConfirmedId = last_confirmation_id
        self.lastReceivedPacket = time.time()

        self.signals = CommunicationSignals()

        self.commsData = CommunicationData(pingerFlag=False,
                                           stateSwitchFlag=False,
                                           valveSwitchFlag=False,
                                           pumpSwitchFlag=False,
                                           heaterSwitchFlag=False,
                                           pingOnce=False,
                                           isCommsOnline=False,
                                           pingInterval=0,
                                           stateToSet=0,
                                           valveId=0,
                                           valveStateToSet=0,
                                           pumpId=0,
                                           heaterId=0,
                                           pumpStateToSet=0,
                                           heaterStateToSet=0,
                                           stateSwitchStartedAt=0,
                                           valveSwitchStartedAt=0,
                                           pumpSwitchStartedAt=0,
                                           heaterSwitchStartedAt=0)

        self.pingRepetitions = 0
        self.stateSwitchRepetitions = 0
        self.valveSwitchRepetitions = 0
        self.pumpSwitchRepetitions = 0
        self.heaterSwitchRepetitions = 0

        self.maxCommandTime = max_command_time * 1000

        self.mechanisms = mechanisms
        self.experimentState = state

        self.lastPingTime = time.time()

        self.maxRepetitions = max_reps

        self.buffer = ""

    @pyqtSlot()
    def run(self):
        received_new = None
        received_last = None
        received_new_list = None
        received_last_list = None
        while True:
            received_new = self.sock_rx.recvfrom(1024)

            # only on Windows
            received_new = received_new[0]

            # print(received_new)
            print(len(received_new))

            # change below length if modifying payload
            if (len(received_new) == 204):
                str_csv = self.convert_bin_uplink_to_old_csv(received_new)
                received_new_list = list(str_csv.split(","))
                self.lastReceivedPacket = time.time()
                print(received_new_list)
                print(len(received_new_list))
                if len(received_new_list) == 65:
                    print(received_new_list)
                    self.signals.input_list.emit(self.createList(received_new_list))
                    self.signals.input_string.emit(str_csv + "\r")
                    print("ok")
                else:
                    print("something went wrong, print to error log file")
            else:
                print("wrong length, print to error log file")

            if self.commsData.pingOnce:
                self.ping()
            if self.commsData.pingerFlag:
                self.pinger()

            if received_new_list != received_last_list and len(received_new_list) == self.bufferLength:
                if self.commsData.stateSwitchFlag:
                    self.switchState(received_new_list[int(self.experimentState)])
                if self.commsData.valveSwitchFlag:
                    self.switchValve(received_new_list[int(self.mechanisms['Valves']['status'])])
                if self.commsData.pumpSwitchFlag:
                    self.switchPump(received_new_list[int(self.mechanisms['Pumps']['status'])])
                if self.commsData.heaterSwitchFlag:
                    self.switchHeater(received_new_list[int(self.mechanisms['Heater']['status'])])
                if int(received_new_list[int(
                        self.lastConnectionConfirmedId)]) > 30 or time.time() - self.lastReceivedPacket > 30 * 1000:
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
        self.sock_tx.sendto(bytes('setState_' + str(self.commsData.stateToSet), encoding='utf8'),
                            (self.ip_tx, self.port_tx))
        if self.commsData.stateToSet != currentState or self.stateSwitchRepetitions <= self.maxRepetitions or time.time() - self.commsData.stateSwitchStartedAt > self.maxCommandTime:
            self.commsData.stateSwitchFlag = False
            self.stateSwitchRepetitions = 0

    def switchValve(self, currentValveState):
        self.sock_tx.sendto(bytes('setValve_' + str(self.commsData.valveId) + '_' + str(self.commsData.valveStateToSet),
                                  encoding='utf8'),
                            (self.ip_tx, self.port_tx))
        if self.commsData.valveStateToSet != currentValveState or self.valveSwitchRepetitions <= self.maxRepetitions or time.time() - self.commsData.valveSwitchStartedAt > self.maxCommandTime:
            self.commsData.valveSwitchFlag = False
            self.valveSwitchRepetitions = 0

    def switchPump(self, currentPumpState):
        self.sock_tx.sendto(
            bytes('setPump_' + str(self.commsData.pumpId) + '_' + str(self.commsData.pumpStateToSet), encoding='utf8'),
            (self.ip_tx, self.port_tx))
        if self.commsData.pumpStateToSet != currentPumpState or self.pumpSwitchRepetitions <= self.maxRepetitions or time.time() - self.commsData.pumpSwitchStartedAt > self.maxCommandTime:
            self.commsData.pumpSwitchFlag = False
            self.pumpSwitchRepetitions = 0

    def switchHeater(self, currentHeaterState):
        self.sock_tx.sendto(
            bytes('setHeater_' + str(self.commsData.heaterId) + '_' + str(self.commsData.heaterStateToSet), encoding='utf8'),
            (self.ip_tx, self.port_tx))
        if self.commsData.pumpStateToSet != currentHeaterState or self.heaterSwitchRepetitions <= self.maxRepetitions or time.time() - self.commsData.heaterSwitchStartedAt > self.maxCommandTime:
            self.commsData.heaterSwitchFlag = False
            self.heaterSwitchRepetitions = 0

    def createList(self, list_to_convert):
        for i in range(2, len(list_to_convert)):
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

    # 2021/08/22,20_59_45,27.25,0,1013.73,1013.61,28.16,1,0.00,0.00,-50.00,0,0,0,0,0,0,0,2,3,1,24.30,50.80,4112,0.00,0.00,4112,0.00,0.00,3088,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0,0,4,0,0,0,0,0,0,0,0.00,0.00,0.00,49
    def convert_bin_uplink_to_old_csv(buf):
        ret_str = ""

        ret_str += str(int.from_bytes(buf[0:2], byteorder='little', signed=False)) + "/"  # year
        ret_str += str(int(buf[2])) + "/"  # month
        ret_str += str(int(buf[3])) + ","  # day
        ret_str += str(int(buf[4])) + "_"  # hour
        ret_str += str(int(buf[5])) + "_"  # minute
        ret_str += str(int(buf[6])) + ","  # second

        ret_str += str(float(int.from_bytes(buf[7:11], byteorder='little', signed=True)) / 100.0) + ","  # rtc temp
        ret_str += str(int.from_bytes(buf[11:13], byteorder='little', signed=False)) + ","  # isDateTimeValid

        ret_str += str(float(int.from_bytes(buf[13:17], byteorder='little', signed=True)) / 100.0) + ","  # pressure(1)
        ret_str += str(
            float(int.from_bytes(buf[17:21], byteorder='little', signed=True)) / 100.0) + ","  # average pressure(1)
        ret_str += str(
            float(int.from_bytes(buf[21:25], byteorder='little', signed=True)) / 100.0) + ","  # pressure temp(1)
        ret_str += str(int(buf[25])) + ","  # pressure(1).isValid

        ret_str += str(float(int.from_bytes(buf[26:30], byteorder='little', signed=True)) / 100.0) + ","  # pressure(2)
        ret_str += str(
            float(int.from_bytes(buf[30:34], byteorder='little', signed=True)) / 100.0) + ","  # average pressure(2)
        ret_str += str(
            float(int.from_bytes(buf[34:38], byteorder='little', signed=True)) / 100.0) + ","  # pressure temp(2)
        ret_str += str(int(buf[38])) + ","  # pressure(2).isValid

        ret_str += str(int.from_bytes(buf[39:43], byteorder='little', signed=True)) + ","  # alt
        ret_str += str(int.from_bytes(buf[43:47], byteorder='little', signed=True)) + ","  # avg alt
        ret_str += str(int(buf[47])) + ","  # alt isValid

        ret_str += str(int.from_bytes(buf[48:52], byteorder='little', signed=True)) + ","  # alt(1)
        ret_str += str(int.from_bytes(buf[52:56], byteorder='little', signed=True)) + ","  # avg alt
        ret_str += str(int(buf[56])) + ","  # alt isValid

        ret_str += str(int.from_bytes(buf[57:61], byteorder='little', signed=True)) + ","  # alt(2)
        ret_str += str(int.from_bytes(buf[61:65], byteorder='little', signed=True)) + ","  # avg alt
        ret_str += str(int(buf[65])) + ","  # alt isValid

        ret_str += str(float(int.from_bytes(buf[66:70], byteorder='little', signed=True)) / 100.0) + ","  # DHT22 temp
        ret_str += str(float(int.from_bytes(buf[70:74], byteorder='little', signed=True)) / 100.0) + ","  # DHT22 hum
        ret_str += str(int.from_bytes(buf[74:76], byteorder='little', signed=False)) + ","  # DHT22 Status
        ret_str += str(float(int.from_bytes(buf[76:80], byteorder='little', signed=True)) / 100.0) + ","  # DHT22 temp
        ret_str += str(float(int.from_bytes(buf[80:84], byteorder='little', signed=True)) / 100.0) + ","  # DHT22 hum
        ret_str += str(int.from_bytes(buf[84:86], byteorder='little', signed=False)) + ","  # DHT22 Status
        ret_str += str(float(int.from_bytes(buf[86:90], byteorder='little', signed=True)) / 100.0) + ","  # DHT22 temp
        ret_str += str(float(int.from_bytes(buf[90:94], byteorder='little', signed=True)) / 100.0) + ","  # DHT22 hum
        ret_str += str(int.from_bytes(buf[94:96], byteorder='little', signed=False)) + ","  # DHT22 Status

        for i in range(20):
            # 20x DS18B20 temps
            ret_str += str(
                float(int.from_bytes(buf[96 + (i * 4):100 + (i * 4)], byteorder='little', signed=True)) / 100.0) + ","

        ret_str += str(int.from_bytes(bytes(buf[176]), byteorder='little', signed=False)) + ","  # pump pwm 1
        ret_str += str(int.from_bytes(bytes(buf[177]), byteorder='little', signed=False)) + ","  # pump pwm 2
        ret_str += str(int.from_bytes(bytes(buf[178]), byteorder='little', signed=False)) + ","  # heating pwm
        ret_str += str(int.from_bytes(buf[179:181], byteorder='little', signed=False)) + ","  # phase

        for i in range(7):
            ret_str += str(int(buf[181 + i])) + ","

        ret_str += str(float(int.from_bytes(buf[188:192], byteorder='little', signed=True)) / 100.0) + ","  # ADC0
        ret_str += str(float(int.from_bytes(buf[192:196], byteorder='little', signed=True)) / 100.0) + ","  # ADC1
        ret_str += str(float(int.from_bytes(buf[196:200], byteorder='little', signed=True)) / 100.0) + ","  # ADC2
        ret_str += str(int.from_bytes(buf[200:204], byteorder='little', signed=False))  # time since last ping

        return ret_str
