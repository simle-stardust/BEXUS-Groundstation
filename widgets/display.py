from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout


class Display(QWidget):

    def __init__(self, *args, structure, units, phases, **kwargs):
        super(Display, self).__init__(*args, **kwargs)

        self.phases = phases

        self.labels = []
        self.indeces = []
        self.unitSymbols = []
        self.primaryKeys = list(structure.keys())

        #Fonts
        self.fontPhaze = QLabel().font()
        self.fontPhaze.setPointSize(32)
        self.fontPhaze.setBold(True)
        self.fontPhaze.setItalic(True)

        self.fontComponentTitle = QLabel().font()
        self.fontComponentTitle.setPointSize(24)
        self.fontComponentTitle.setBold(True)

        self.fontComponentSensor = QLabel().font()
        self.fontComponentSensor.setPointSize(12)
        self.fontComponentSensor.setItalic(True)

        self.fontComponentVariable = QLabel().font()
        self.fontComponentVariable.setPointSize(12)

        self.fontAltitudeVariable = QLabel().font()
        self.fontAltitudeVariable.setPointSize(24)

        #MAIN LAYOUT
        self.layoutMain = QVBoxLayout()

        #LAYOUT WITH DIFFERENT TYPES OF DATA ON THE TOP LAYER
        self.layoutComponentsTop = QHBoxLayout()
        self.layoutMain.addLayout(self.layoutComponentsTop)

        #ALTITUDE
        #creating layout:
        self.layoutAltitude = QHBoxLayout()
        self.layoutComponentsTop.addLayout(self.layoutAltitude)
        self.layoutAltitude.setAlignment(Qt.AlignLeft)
        #creating labels:
        self.labelAltitudeTitle = QLabel(str(self.primaryKeys[2]).capitalize() + ': ')
        self.layoutAltitude.addWidget(self.labelAltitudeTitle)
        self.labelAltitudeTitle.setFont(self.fontComponentTitle)
        self.labelAltitudeTitle.setAlignment(Qt.AlignRight)
        self.labelAltitudeCurrent = QLabel("-----")
        self.layoutAltitude.addWidget(self.labelAltitudeCurrent)
        self.labelAltitudeCurrent.setFont(self.fontAltitudeVariable)
        self.labelAltitudeCurrent.setAlignment(Qt.AlignLeft)
        #adding label, index and unit to lists:
        self.labels.append(self.labelAltitudeCurrent)
        self.indeces.append(int(structure[self.primaryKeys[2]]))
        self.unitSymbols.append(units[str(self.primaryKeys[2]).lower()]['symbol'])

        #EXPERIMENT PHAZE
        #creating label:
        self.labelPhaze = QLabel("Placeholder_Phase ")
        self.labelPhaze.setAlignment(Qt.AlignRight)
        self.labelPhaze.setFont(self.fontPhaze)
        self.layoutComponentsTop.addWidget(self.labelPhaze)
        #inserting label and index to lists:
        self.labels.insert(0, self.labelPhaze)
        self.indeces.insert(0, int(structure[self.primaryKeys[0]]))
        self.unitSymbols.insert(0, 'blank')

        #LAYOUT IN THE MIDDLE LAYER (used as spacer)
        #creating layout with blank label:
        self.layoutComponentsMiddle = QHBoxLayout()
        self.layoutComponentsMiddle.addWidget(QLabel(""))
        self.layoutMain.addLayout(self.layoutComponentsMiddle)

        #LAYOUT WITH DIFFERENT TYPES OF DATA ON THE BOTTOM LAYER (fully loaded from config)
        #creating layout:
        self.layoutComponentsBottom = QHBoxLayout()
        self.layoutMain.addLayout(self.layoutComponentsBottom)

        #LOYOUTS AND LABELS GENERATED IN ACCORDANCE WITH config.hjson
        self.objects = []
        for i in range(3,len(structure)):
            #layouts with categories:
            self.objects.append(QVBoxLayout())
            self.objects[-1].setAlignment(Qt.AlignTop)
            self.layoutComponentsBottom.addLayout(self.objects[-1])
            self.objects.append(QLabel(str(self.primaryKeys[i]).capitalize()))
            self.objects[-1].setAlignment(Qt.AlignCenter)
            self.objects[-1].setFont(self.fontComponentTitle)
            self.objects[-2].addWidget(self.objects[-1])
            #auxiliary horizontal layout:
            self.objects.append(QHBoxLayout())
            self.objects[-3].addLayout(self.objects[-1])
            self.tempAuxiliaryLayout = self.objects[-1]
            #vertical layouts for columns of data:
            for j in range(len(structure[self.primaryKeys[i]])):
                self.secondaryKeys = list(structure[self.primaryKeys[i]].keys())
                self.objects.append(QVBoxLayout())
                if j == 0:
                    self.objects[-1].setAlignment(Qt.AlignRight)
                elif j < len(structure[self.primaryKeys[i]])-1:
                    self.objects[-1].setAlignment(Qt.AlignCenter)
                else:
                    self.objects[-1].setAlignment(Qt.AlignLeft)
                self.tempAuxiliaryLayout.addLayout(self.objects[-1])
                self.tempColumnLayout = self.objects[-1]
                #small headers with info about what is in columns below them:
                self.objects.append(QLabel(str(self.secondaryKeys[j])))
                self.tempColumnLayout.addWidget(self.objects[-1])
                #names of sensors (j=0) and readings (j>0):
                for k in range(len(structure[self.primaryKeys[i]][self.secondaryKeys[j]])):
                    if j == 0:
                        self.objects.append(QLabel(str(structure[self.primaryKeys[i]][self.secondaryKeys[j]][k]).lower()))
                        self.objects[-1].setFont(self.fontComponentSensor)
                        self.tempColumnLayout.addWidget(self.objects[-1])
                    else:
                        self.objects.append(QLabel("--"))
                        self.objects[-1].setFont(self.fontComponentVariable)
                        self.tempColumnLayout.addWidget(self.objects[-1])
                        #adding label, index and unit to lists:
                        self.labels.append(self.objects[-1])
                        self.indeces.append(int(structure[self.primaryKeys[i]][self.secondaryKeys[j]][k]))
                        if self.primaryKeys[i] == 'Temperature':
                            self.unitSymbols.append('°C')
                        else:
                            self.unitSymbols.append(units[str(self.primaryKeys[i]).lower()]['symbol'])

        #some clearing
        del self.tempAuxiliaryLayout
        del self.tempColumnLayout
        self.secondaryKeys.clear()
        del self.secondaryKeys
        self.primaryKeys.clear()
        del self.primaryKeys

        #setting layout for custom widget
        self.setLayout(self.layoutMain)

    def update(self, input):
        self.labels[0].setText(self.phases[input[self.indeces[0]]] + ' ')
        for u in range(1,len(self.labels)):
            self.labels[u].setText(str(input[self.indeces[u]]) + self.unitSymbols[u])