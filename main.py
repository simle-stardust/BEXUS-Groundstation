from PyQt5 import QtGui
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QTabWidget, QScrollArea
from widgets.display import Display
from widgets.mechanisms import Mechanisms
from widgets.sensors import Sensors
from widgets.table import Table
from widgets.charts import Charts
from pyqtgraph.console import ConsoleWidget
from widgets.buttons import Buttons

from threads.communication import Communication

import hjson
from datetime import date
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Stardust Ground Station")
        self.setWindowIcon(QtGui.QIcon('images/stardust.ico'))
        self.resize(1000, 600)

        self.logFile = 'logs/StardustGroundStation' + str(date.today()) + '.txt'

        with open("config.hjson", "r") as file:
            config = hjson.load(file)

        self.layout = QVBoxLayout()

        self.updatableWidgets = []

        self.display = Display(structure=config['basics'], units=config['units'], phases=config['phases'])
        self.layout.addWidget(self.display)
        self.updatableWidgets.append(self.display)

        self.tabsTop = QTabWidget()
        self.layout.addWidget(self.tabsTop)

        self.sensors = Sensors(structure=config['sensors'], units=config['units'])
        self.tabsTop.addTab(self.sensors, 'Sensors')
        self.updatableWidgets.append(self.sensors)

        self.mechanisms = Mechanisms(structure=config['mechanisms'], statuses=config['statuses'])
        self.tabsTop.addTab(self.mechanisms, 'Mechanisms')
        self.updatableWidgets.append(self.mechanisms)

        self.tabsBottom = QTabWidget()
        self.layout.addWidget(self.tabsBottom)

        if config['table']:
            self.table = Table(header_labels=config['labels'], max_size=config['maxSize'])
            self.updatableWidgets.append(self.table)
            self.tabsBottom.addTab(self.table, 'Table')
        if config['charts']:
            self.charts = Charts(structure=config['sensors'], units=config['units'],
                                 time_index=config['basics'][list(config['basics'].keys())[2]])
            self.updatableWidgets.append(self.charts)
            self.scrollCharts = QScrollArea()
            self.scrollCharts.setWidgetResizable(True)
            self.scrollCharts.setWidget(self.charts)
            self.tabsBottom.addTab(self.scrollCharts, 'Charts')
        if config['console']:
            self.console = ConsoleWidget()
            self.tabsBottom.addTab(ConsoleWidget(), 'Console')
        if config['buttons']:
            self.buttons = Buttons(phases=config['phases'], valves=config['mechanisms']['Valves']['name'], valvestatuses=config['statuses']['valves'], pumps=config['mechanisms']['Pumps']['name'])
            self.updatableWidgets.append(self.buttons)
            self.tabsBottom.addTab(self.buttons, 'Function Buttons')

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.testDataRandom = []

        self.receiversThreadPool = QThreadPool()

        self.comms = None
        self.communicate(ip_rx=config['UDP_rx']['ip'], port_rx=config['UDP_rx']['port'], ip_tx=config['UDP_tx']['ip'], port_tx=config['UDP_tx']['port'],buffer=len(list(config['labels'])), mechs=config['mechanisms'], status=config['basics']['Altitude'], last_ping=int(config['lastPing']))

        del config

    def updateGUI(self, data):
        for widget in self.updatableWidgets:
            if type(widget) is Buttons:
                widget.updateGUI(new_comms_data=self.comms.commsData)
                self.comms.commsData = widget.commsData
            else:
                widget.updateGUI(data)

    def printToFile(self, data):
        file = open(self.logFile, 'a+')
        file.write(data)
        file.close()

    def communicate(self, ip_rx, port_rx, ip_tx, port_tx, mechs, status, buffer, last_ping):
        self.comms = Communication(ip_rx=ip_rx, port_rx=port_rx, ip_tx=ip_tx, port_tx=port_tx, max_reps=10, mechanisms=mechs, state=status, max_command_time=20, buffer_len=buffer, last_ping_time=last_ping)
        self.comms.signals.input_list.connect(self.updateGUI)
        self.comms.signals.input_string.connect(self.printToFile)
        self.receiversThreadPool.start(self.comms)


def test():
    print("Test")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())
