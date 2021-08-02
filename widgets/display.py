from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout


class Display(QWidget):

    def __init__(self, *args, structure, units, phases, **kwargs):
        super(Display, self).__init__(*args, **kwargs)

        self.phases = phases

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
        self.labelAltitudeTitle = QLabel(str(self.primaryKeys[0]).capitalize() + ': ')
        self.layoutAltitude.addWidget(self.labelAltitudeTitle)
        self.labelAltitudeTitle.setFont(self.fontComponentTitle)
        self.labelAltitudeTitle.setAlignment(Qt.AlignRight)
        self.labelAltitudeCurrent = QLabel("-----")
        self.layoutAltitude.addWidget(self.labelAltitudeCurrent)
        self.labelAltitudeCurrent.setFont(self.fontAltitudeVariable)
        self.labelAltitudeCurrent.setAlignment(Qt.AlignLeft)
        #adding label, index and unit to lists:
        self.indeces.append(int(structure[self.primaryKeys[0]]))
        self.altitudeUnitSymbol = units[str(self.primaryKeys[0]).lower()]['symbol']

        #EXPERIMENT PHAZE
        #creating label:
        self.labelPhaze = QLabel("Placeholder_Phase ")
        self.labelPhaze.setAlignment(Qt.AlignRight)
        self.labelPhaze.setFont(self.fontPhaze)
        self.layoutComponentsTop.addWidget(self.labelPhaze)
        #inserting label and index to lists:
        self.indeces.append(int(structure[self.primaryKeys[1]]))

        #TODO prawdziwy spacer(?)
        #LAYOUT IN THE MIDDLE LAYER (used as spacer)
        #creating layout with blank label:
        #self.layoutComponentsMiddle = QHBoxLayout()
        #self.layoutComponentsMiddle.addWidget(QLabel(""))
        #self.layoutMain.addLayout(self.layoutComponentsMiddle)

        #some clearing
        self.primaryKeys.clear()
        del self.primaryKeys

        #setting layout for custom widget
        self.setLayout(self.layoutMain)

    def updateGUI(self, data):
        self.labelAltitudeCurrent.setText(str(data[self.indeces[0]]) + self.altitudeUnitSymbol)
        self.labelPhaze.setText(self.phases[data[self.indeces[1]]] + ' ')