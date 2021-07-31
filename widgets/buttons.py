from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox, QDoubleSpinBox

from threads.senders.pinger import Pinger
from threads.senders.stateSwitcher import StateSwitcher
from threads.senders.valveSwitcher import ValveSwitcher
from threads.senders.pumpSwitcher import PumpSwitcher

import socket


class Buttons(QWidget):

    def __init__(self, *args, socket, udp_ip_tx, udp_port_tx, **kwargs):
        super(Buttons, self).__init__(*args, **kwargs)

        self.fontTitle = QLabel().font()
        self.fontTitle.setPointSize(24)
        self.fontTitle.setBold(True)

        self.layoutMain = QHBoxLayout()
        self.layoutMain.setAlignment(Qt.AlignVCenter)

        self.layoutSetters = QVBoxLayout()

        self.layoutSetterState = QVBoxLayout()
        self.layoutSetterState.setAlignment(Qt.AlignTop)
        self.labelState = QLabel("Experiment Status")
        self.labelState.setFont(self.fontTitle)
        self.labelState.setAlignment(Qt.AlignCenter)
        self.layoutSetterState.addWidget(self.labelState)
        self.experimentStateBox = QComboBox()
        self.layoutSetterState.addWidget(self.experimentStateBox)
        self.setStateButton = QPushButton("SET")

        self.setStateButton.clicked.connect(self.setStateButtonOnClick)

        self.layoutSetterState.addWidget(self.setStateButton)
        self.layoutSetters.addLayout(self.layoutSetterState)

        self.layoutSetterValve = QVBoxLayout()
        self.layoutSetterValve.setAlignment(Qt.AlignTop)
        self.labelValve = QLabel("Valves")
        self.labelValve.setFont(self.fontTitle)
        self.labelValve.setAlignment(Qt.AlignCenter)
        self.layoutSetterValve.addWidget(self.labelValve)
        self.valveBox = QComboBox()
        self.layoutSetterValve.addWidget(self.valveBox)
        self.valveStateBox = QComboBox()
        self.layoutSetterValve.addWidget(self.valveStateBox)
        self.setValveButton = QPushButton("SET")

        self.setValveButton.clicked.connect(self.setValveButtonOnClick)

        self.layoutSetterValve.addWidget(self.setValveButton)
        self.layoutSetters.addLayout(self.layoutSetterValve)

        self.layoutSetterPump = QVBoxLayout()
        self.layoutSetterPump.setAlignment(Qt.AlignTop)
        self.labelPump = QLabel("Pumps")
        self.labelPump.setFont(self.fontTitle)
        self.labelPump.setAlignment(Qt.AlignCenter)
        self.layoutSetterPump.addWidget(self.labelPump)
        self.pumpBox = QComboBox()
        self.layoutSetterPump.addWidget(self.pumpBox)
        self.pumpStateBox = QDoubleSpinBox()
        self.pumpStateBox.setMaximum(255)
        self.layoutSetterPump.addWidget(self.pumpStateBox)
        self.setPumpButton = QPushButton("SET")

        self.setPumpButton.clicked.connect(self.setPumpButtonOnClick)

        self.layoutSetterPump.addWidget(self.setPumpButton)
        self.layoutSetters.addLayout(self.layoutSetterPump)

        self.layoutPinger = QVBoxLayout()
        self.layoutPinger.setAlignment(Qt.AlignCenter)
        self.layoutP1 = QHBoxLayout()
        self.labelPing = QLabel("Ping")
        self.labelPing.setFont(self.fontTitle)
        self.labelPing.setAlignment(Qt.AlignCenter)
        self.layoutP1.addWidget(self.labelPing)
        self.layoutP2 = QHBoxLayout()
        self.ledLbl = QLabel()
        self.ledImg = QPixmap('images/red-led.png')
        self.ledImg = self.ledImg.scaled(25, 25, QtCore.Qt.KeepAspectRatio)
        self.ledLbl.setPixmap(self.ledImg)
        self.layoutP2.addWidget(self.ledLbl)
        self.pingButton = QPushButton("                    PING                    ")
        self.pingButton.clicked.connect(self.singlePing)
        self.layoutP2.addWidget(self.pingButton)
        self.layoutP3 = QHBoxLayout()
        self.autoPingCheck = QCheckBox()
        self.autoPingCheck.stateChanged.connect(self.startPinging)
        self.layoutP3.addWidget(self.autoPingCheck)
        self.labelAutoPing1 = QLabel(" auto-ping in ")
        self.layoutP3.addWidget(self.labelAutoPing1)
        self.intervalBox = QDoubleSpinBox()
        self.intervalBox.setMinimum(1)
        self.layoutP3.addWidget(self.intervalBox)
        self.labelAutoPing2 = QLabel(" intervals")
        self.layoutP3.addWidget(self.labelAutoPing2)

        self.layoutPinger.addLayout(self.layoutP1)
        self.layoutPinger.addLayout(self.layoutP2)
        self.layoutPinger.addLayout(self.layoutP3)

        self.layoutMain.addLayout(self.layoutSetters)
        self.layoutMain.addLayout(self.layoutPinger)

        self.setLayout(self.layoutMain)

        self.sendersThreadPool = QThreadPool()
        self.pinger = None

        self.socket = socket
        self.tx_ip = udp_ip_tx
        self.tx_port = udp_port_tx

    def updateGUI(self, data):
        if not self.setStateButton.isEnabled():
            if int(self.experimentStateBox.currentIndex()) == data[self.experimentStateBox.currentIndex()]:
                self.setStateButton.setEnabled(True)
                self.experimentStateBox.setEnabled(True)
        if not self.setValveButton.isEnabled():
            if int(self.valveStateBox.currentIndex()) == data[self.valveBox.currentIndex()]:
                self.setValveButton.setEnabled(True)
                self.valveBox.setEnabled(True)
                self.valveStateBox.setEnabled(True)
        if not self.setPumpButton.isEnabled():
            if int(self.pumpStateBox.value()) == data[self.pumpBox.currentIndex()]:
                self.setPumpButton.setEnabled(True)
                self.pumpBox.setEnabled(True)
                self.pumpStateBox.setEnabled(True)

    def singlePing(self):
        #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.bind((self.udpIP, self.udpPort))
        self.socket.sendto(bytes("ping", encoding='utf8'), (self.tx_ip, self.tx_port))
        print("ping")

    def startPinging(self):
        if (self.autoPingCheck.isChecked()):
            self.pinger = Pinger(t=self.intervalBox.value(), sock=self.socket, ip_tx=self.tx_ip, port_tx=self.tx_port)
            self.sendersThreadPool.start(self.pinger)
        else:
            self.pinger.ifPing = False

    def setStateButtonOnClick(self):
        self.setStateButton.setEnabled(False)
        self.experimentStateBox.setEnabled(False)
        state_switcher = StateSwitcher(expected=self.experimentStateBox.currentIndex(), sock=self.socket, ip_tx=self.tx_ip, port_tx=self.tx_port)
        self.sendersThreadPool.start(state_switcher)

    def setValveButtonOnClick(self):
        self.setValveButton.setEnabled(False)
        self.valveBox.setEnabled(False)
        self.valveStateBox.setEnabled(False)
        valve_switcher = ValveSwitcher(index=self.valveBox.currentIndex(), expected=self.valveStateBox.currentIndex(), sock=self.socket, ip_tx=self.tx_ip, port_tx=self.tx_port)
        self.sendersThreadPool.start(valve_switcher)

    def setPumpButtonOnClick(self):
        self.pumpBox.setEnabled(False)
        self.pumpStateBox.setEnabled(False)
        pump_switcher = PumpSwitcher(index=self.pumpBox.currentIndex(), expected=int(self.pumpStateBox.value()), sock=self.socket, ip_tx=self.tx_ip, port_tx=self.tx_port)
        self.sendersThreadPool.start(pump_switcher)
