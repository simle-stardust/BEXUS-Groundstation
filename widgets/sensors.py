from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout


class Sensors(QWidget):

    def __init__(self, *args, structure, units, **kwargs):
        super(Sensors, self).__init__(*args, **kwargs)

        self.labels = []
        self.indeces = []
        self.unitSymbols = []
        self.primaryKeys = list(structure.keys())

        # Fonts
        self.fontComponentTitle = QLabel().font()
        self.fontComponentTitle.setPointSize(24)
        self.fontComponentTitle.setBold(True)

        self.fontComponentSensor = QLabel().font()
        self.fontComponentSensor.setPointSize(12)
        self.fontComponentSensor.setItalic(True)

        self.fontComponentVariable = QLabel().font()
        self.fontComponentVariable.setPointSize(12)

        # MAIN LAYOUT
        self.layoutMain = QHBoxLayout()
        self.layoutMain.addLayout(self.layoutMain)

        # LOYOUTS AND LABELS GENERATED IN ACCORDANCE WITH config.hjson
        self.objects = []
        for i in range(len(structure)):
            # layouts with categories:
            self.objects.append(QVBoxLayout())
            self.objects[-1].setAlignment(Qt.AlignTop)
            self.layoutMain.addLayout(self.objects[-1])
            self.objects.append(QLabel(str(self.primaryKeys[i]).capitalize()))
            self.objects[-1].setAlignment(Qt.AlignCenter)
            self.objects[-1].setFont(self.fontComponentTitle)
            self.objects[-2].addWidget(self.objects[-1])
            # auxiliary horizontal layout:
            self.objects.append(QHBoxLayout())
            self.objects[-3].addLayout(self.objects[-1])
            self.tempAuxiliaryLayout = self.objects[-1]
            # vertical layouts for columns of data:
            for j in range(len(structure[self.primaryKeys[i]])):
                self.secondaryKeys = list(structure[self.primaryKeys[i]].keys())
                self.objects.append(QVBoxLayout())
                if j == 0:
                    self.objects[-1].setAlignment(Qt.AlignRight)
                elif j < len(structure[self.primaryKeys[i]]) - 1:
                    self.objects[-1].setAlignment(Qt.AlignCenter)
                else:
                    self.objects[-1].setAlignment(Qt.AlignLeft)
                self.tempAuxiliaryLayout.addLayout(self.objects[-1])
                self.tempColumnLayout = self.objects[-1]
                # small headers with info about what is in columns below them:
                self.objects.append(QLabel(str(self.secondaryKeys[j])))
                self.tempColumnLayout.addWidget(self.objects[-1])
                # names of sensors (j=0) and readings (j>0):
                for k in range(len(structure[self.primaryKeys[i]][self.secondaryKeys[j]])):
                    if j == 0:
                        self.objects.append(
                            QLabel(str(structure[self.primaryKeys[i]][self.secondaryKeys[j]][k]).lower()))
                        self.objects[-1].setFont(self.fontComponentSensor)
                        self.tempColumnLayout.addWidget(self.objects[-1])
                    else:
                        self.objects.append(QLabel("--"))
                        self.objects[-1].setFont(self.fontComponentVariable)
                        self.tempColumnLayout.addWidget(self.objects[-1])
                        # adding label, index and unit to lists:
                        self.labels.append(self.objects[-1])
                        self.indeces.append(int(structure[self.primaryKeys[i]][self.secondaryKeys[j]][k]))
                        if self.primaryKeys[i] == 'Temperature':
                            self.unitSymbols.append('°C')
                        else:
                            self.unitSymbols.append(units[str(self.primaryKeys[i]).lower()]['symbol'])

        # some clearing
        del self.tempAuxiliaryLayout
        del self.tempColumnLayout
        self.secondaryKeys.clear()
        del self.secondaryKeys
        self.primaryKeys.clear()
        del self.primaryKeys

        # setting layout for custom widget
        self.setLayout(self.layoutMain)

    def updateGUI(self, data):
        for u in range(len(self.labels)):
            self.labels[u].setText(str(data[self.indeces[u]]) + self.unitSymbols[u])
