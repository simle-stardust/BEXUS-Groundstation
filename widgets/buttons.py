from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox, QDoubleSpinBox

from datastructures.communicationdata import CommunicationData


class Buttons(QWidget):

    def __init__(self, *args, **kwargs):
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
        self.ledImgOn = QPixmap('images/green-led.png')
        self.ledImgOff = QPixmap('images/red-led.png')
        self.ledImgOn = self.ledImgOn.scaled(25, 25, QtCore.Qt.KeepAspectRatio)
        self.ledImgOff = self.ledImgOff.scaled(25, 25, QtCore.Qt.KeepAspectRatio)
        self.ledLbl.setPixmap(self.ledImgOff)
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

        self.commsData = CommunicationData(pingerFlag=False,
                                           stateSwitchFlag=False,
                                           valveSwitchFlag=False,
                                           pumpSwitchFlag=False,
                                           isCommsOnline=False,
                                           pingOnce=False,
                                           pingInterval=0,
                                           stateToSet=0,
                                           valveId=0,
                                           valveStateToSet=0,
                                           pumpId=0,
                                           pumpStateToSet=0,
                                           stateSwitchStartedAt=0,
                                           valveSwitchStartedAt=0,
                                           pumpSwitchStartedAt=0)

    def updateGUI(self, new_comms_data):
        if self.commsData.isCommsOnline != new_comms_data.isCommsOnline:
            if new_comms_data.isCommsOnline:
                self.ledLbl.setPixmap(self.ledImgOn)
            else:
                self.ledLbl.setPixmap(self.ledImgOff)
        self.commsData = new_comms_data
        if self.setStateButton.isEnabled():
            if self.commsData.stateSwitchFlag:
                self.setStateButton.setEnabled(True)
                self.experimentStateBox.setEnabled(True)
        if self.setValveButton.isEnabled():
            if self.commsData.valveSwitchFlag:
                self.setValveButton.setEnabled(True)
                self.valveBox.setEnabled(True)
                self.valveStateBox.setEnabled(True)
        if self.setPumpButton.isEnabled():
            if self.commsData.pumpSwitchFlag:
                self.setPumpButton.setEnabled(True)
                self.pumpBox.setEnabled(True)
                self.pumpStateBox.setEnabled(True)

    def singlePing(self):
        self.commsData.pingOnce = True

    def startPinging(self):
        if self.autoPingCheck.isChecked():
            self.commsData.pingerFlag = True

    def setStateButtonOnClick(self):
        self.setStateButton.setEnabled(False)
        self.experimentStateBox.setEnabled(False)
        self.commsData.stateToSet = self.experimentStateBox.currentIndex()
        self.commsData.stateSwitchFlag = True

    def setValveButtonOnClick(self):
        self.setValveButton.setEnabled(False)
        self.valveBox.setEnabled(False)
        self.valveStateBox.setEnabled(False)
        self.commsData.valveId = self.valveBox.currentIndex()
        self.commsData.valveStateToSet = self.valveStateBox.currentIndex()
        self.commsData.valveSwitchFlag = True

    def setPumpButtonOnClick(self):
        self.pumpBox.setEnabled(False)
        self.pumpStateBox.setEnabled(False)
        self.commsData.pumpId = self.pumpBox.currentIndex()
        self.commsData.pumpStateToSet = self.pumpStateBox.value()
        self.commsData.pumpSwitchFlag = True
