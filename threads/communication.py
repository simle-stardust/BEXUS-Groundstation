import socket
import time

from datetime import datetime

from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal


#2021/08/22,20_59_45,27.25,0,1013.73,1013.61,28.16,1,0.00,0.00,-50.00,0,0,0,0,0,0,0,2,3,1,24.30,50.80,4112,0.00,0.00,4112,0.00,0.00,3088,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0,0,4,0,0,0,0,0,0,0,0.00,0.00,0.00,49
def convert_bin_uplink_to_old_csv(buf):
    ret_str = ""

    ret_str += str(int.from_bytes(buf[0:2], byteorder='little', signed=False)) + "/" #year
    ret_str += str(int(buf[2])) + "/" #month
    ret_str += str(int(buf[3])) + "," #day
    ret_str += str(int(buf[4])) + "_" #hour
    ret_str += str(int(buf[5])) + "_" #minute
    ret_str += str(int(buf[6])) + "," #second

    ret_str += str(float(int.from_bytes(buf[7:11], byteorder='little', signed=True))/100.0) + "," #rtc temp
    ret_str += str(int.from_bytes(buf[11:13], byteorder='little', signed=False)) + "," #isDateTimeValid

    ret_str += str(float(int.from_bytes(buf[13:17], byteorder='little', signed=True))/100.0) + "," #pressure(1)
    ret_str += str(float(int.from_bytes(buf[17:21], byteorder='little', signed=True))/100.0) + "," #average pressure(1)
    ret_str += str(float(int.from_bytes(buf[21:25], byteorder='little', signed=True))/100.0) + "," #pressure temp(1)
    ret_str += str(int(buf[25])) + "," #pressure(1).isValid

    ret_str += str(float(int.from_bytes(buf[26:30], byteorder='little', signed=True))/100.0) + "," #pressure(2)
    ret_str += str(float(int.from_bytes(buf[30:34], byteorder='little', signed=True))/100.0) + "," #average pressure(2)
    ret_str += str(float(int.from_bytes(buf[34:38], byteorder='little', signed=True))/100.0) + "," #pressure temp(2)
    ret_str += str(int(buf[38])) + "," #pressure(2).isValid

    ret_str += str(int.from_bytes(buf[39:43], byteorder='little', signed=True)) + "," #alt
    ret_str += str(int.from_bytes(buf[43:47], byteorder='little', signed=True)) + "," #avg alt
    ret_str += str(int(buf[47])) + "," #alt isValid

    ret_str += str(int.from_bytes(buf[48:52], byteorder='little', signed=True)) + "," #alt(1)
    ret_str += str(int.from_bytes(buf[52:56], byteorder='little', signed=True)) + "," #avg alt
    ret_str += str(int(buf[56])) + "," #alt isValid

    ret_str += str(int.from_bytes(buf[57:61], byteorder='little', signed=True)) + "," #alt(2)
    ret_str += str(int.from_bytes(buf[61:65], byteorder='little', signed=True)) + "," #avg alt
    ret_str += str(int(buf[65])) + "," #alt isValid

    ret_str += str(float(int.from_bytes(buf[66:70], byteorder='little', signed=True))/100.0) + "," #DHT22 temp
    ret_str += str(float(int.from_bytes(buf[70:74], byteorder='little', signed=True))/100.0) + "," #DHT22 hum
    ret_str += str(int.from_bytes(buf[74:76], byteorder='little', signed=False)) + "," #DHT22 Status
    ret_str += str(float(int.from_bytes(buf[76:80], byteorder='little', signed=True))/100.0) + "," #DHT22 temp
    ret_str += str(float(int.from_bytes(buf[80:84], byteorder='little', signed=True))/100.0) + "," #DHT22 hum
    ret_str += str(int.from_bytes(buf[84:86], byteorder='little', signed=False)) + "," #DHT22 Status
    ret_str += str(float(int.from_bytes(buf[86:90], byteorder='little', signed=True))/100.0) + "," #DHT22 temp
    ret_str += str(float(int.from_bytes(buf[90:94], byteorder='little', signed=True))/100.0) + "," #DHT22 hum
    ret_str += str(int.from_bytes(buf[94:96], byteorder='little', signed=False)) + "," #DHT22 Status

    for i in range(20):
        # 20x DS18B20 temps
        ret_str += str(float(int.from_bytes(buf[96 + (i*4):100 + (i*4)], byteorder='little', signed=True))/100.0) + ","

    ret_str += str(int.from_bytes(bytes(buf[176]), byteorder='little', signed=False)) + "," #pump pwm 1
    ret_str += str(int.from_bytes(bytes(buf[177]), byteorder='little', signed=False)) + "," #pump pwm 2
    ret_str += str(int.from_bytes(bytes(buf[178]), byteorder='little', signed=False)) + "," #heating pwm
    ret_str += str(int.from_bytes(buf[179:181], byteorder='little', signed=False)) + "," #phase    
    
    for i in range(7):
        ret_str += str(int(buf[181+i])) + ","

    ret_str += str(float(int.from_bytes(buf[188:192], byteorder='little', signed=True))/100.0) + "," #ADC0
    ret_str += str(float(int.from_bytes(buf[192:196], byteorder='little', signed=True))/100.0) + "," #ADC1
    ret_str += str(float(int.from_bytes(buf[196:200], byteorder='little', signed=True))/100.0) + "," #ADC2
    ret_str += str(float(int.from_bytes(buf[200:204], byteorder='little', signed=True))/100.0) + "," #ADC3
    ret_str += str(int.from_bytes(buf[204:208], byteorder='little', signed=False)) #time since last ping

    return ret_str

class CommunicationSignals(QObject):

    input_list = pyqtSignal(list)
    input_string = pyqtSignal(str)


class Communication(QRunnable):

    def __init__(self, sock_rx, sock_tx, ip_tx, port_tx, interval):
        super(Communication, self).__init__()

        self.sock_rx = sock_rx
        self.sock_tx = sock_tx
        self.ip_tx = ip_tx 
        self.port_tx = port_tx

        self.signals = CommunicationSignals()

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

        self.maxRepetitions = 1

        self.stateToSet = None
        self.currentState = None

        self.valveId = None
        self.valveStateToSet = None
        self.currentValveState = None

        self.pumpId = None
        self.pumpStateToSet = None
        self.currentPumpState = None


    @pyqtSlot()
    def run(self):
        received_new = None
        received_last = None
        while True:
            received_new = self.sock_rx.recvfrom(1024)

            #only on Windows
            received_new = received_new[0]

            #print(received_new)
            print(len(received_new))

            # change below length if modifying payload
            if (len(received_new) == 208):
                str_csv = convert_bin_uplink_to_old_csv(received_new)
                received_new_list = list(str_csv.split(","))
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
#
        #   if "@" in self.buffer and ";" in self.buffer:

        #       received_new_list = list(self.buffer[self.buffer.find("@")+1 : self.buffer.find(";")].split(","))
        #       if len(received_new_list) == 1:
        #           #error, flush the buffer up to "@"
        #           self.buffer=self.buffer[self.buffer.find("@"):]
        #       else:
        #           #print(received_new_list)
        #           print(len(received_new_list))
        #           # only update data when all required fields are present
        #           if len(received_new_list) == 65:
        #               print(received_new_list)
        #               self.signals.input_list.emit(self.createList(received_new_list))
        #               self.signals.input_string.emit(self.buffer + "\r")
        #           self.buffer=""

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
        if self.stateToSet != self.currentState or self.stateSwitchRepetitions < self.maxRepetitions:
            self.stateSwitchFlag = False
            self.stateSwitchRepetitions = 0

    def switchValve(self):
        self.sock_tx.sendto(bytes('setValve_' + str(self.valveId) + str(self.valveStateToSet), encoding='utf8'), (self.ip_tx, self.port_tx))
        if self.valveStateToSet != self.currentValveState or self.valveSwitchRepetitions < self.maxRepetitions:
            self.valveSwitchFlag = False
            self.valveSwitchRepetitions = 0
            
    def switchPump(self):
        self.sock_tx.sendto(bytes('setPump_' + str(self.pumpId) + '_' + str(self.pumpStateToSet), encoding='utf8'), (self.ip_tx, self.port_tx))
        if self.pumpStateToSet != self.currentPumpState or self.pumpSwitchRepetitions < self.maxRepetitions:
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