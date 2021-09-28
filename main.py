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

from threads.receivers.tester import Tester
from threads.communication import Communication

from threads.blank import Blank

import hjson
from datetime import date
import sys
import socket


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Stardust Ground Station")
        self.setWindowIcon(QtGui.QIcon('images/stardust.ico'))
        self.resize(1000, 600)

        self.logFile = 'logs/StardustGroundStation' + str(date.today()) + '.txt'
        self.logErrorFile = 'logs/StardustGroundStation' + str(date.today()) + '_error.txt'

        with open("config.hjson", "r") as file:
            config = hjson.load(file)

        self.sock_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.ip_rx = config['UDP_rx']['ip']
        self.port_rx = int(config['UDP_rx']['port'])

        self.ip_tx = config['UDP_tx']['ip']
        self.port_tx = int(config['UDP_tx']['port'])
        
        self.sock_rx.bind((self.ip_rx, self.port_rx))

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
                                 time_index=config['basics']['time'])
            self.updatableWidgets.append(self.charts)
            self.scrollCharts = QScrollArea()
            self.scrollCharts.setWidgetResizable(True)
            self.scrollCharts.setWidget(self.charts)
            self.tabsBottom.addTab(self.scrollCharts, 'Charts')
        if config['console']:
            self.console = ConsoleWidget()
            self.tabsBottom.addTab(ConsoleWidget(), 'Console')
        if config['buttons']:
            self.buttons = Buttons(socket=self.sock_tx, udp_ip_tx=self.ip_tx, udp_port_tx=self.port_tx, phases=config['phases'], valves=config['mechanisms']['Valves']['name'], valvestatuses=config['statuses']['valves'], pumps=config['mechanisms']['PWMs']['name'])
            self.updatableWidgets.append(self.buttons)
            self.tabsBottom.addTab(self.buttons, 'Function Buttons')

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.testDataRandom = []

        self.receiversThreadPool = QThreadPool()

        #self.testing()
        #self.blanking()

        self.communicate()

        del config

    def updateGUI(self, data):
        for widget in self.updatableWidgets:
            widget.updateGUI(data)
        print(self.receiversThreadPool.activeThreadCount())

    def printToFile(self, data):
        file = open(self.logFile, 'a+')
        file.write(data)
        file.close()

    def testing(self):
        tester = Tester(self)
        tester.signals.result.connect(self.updateGUI)
        self.receiversThreadPool.start(tester)

    def communicate(self):
        comms = Communication(self.sock_rx, self.sock_tx, self.ip_tx, self.port_tx, 60, self.logErrorFile)
        comms.signals.input_list.connect(self.updateGUI)
        comms.signals.input_string.connect(self.printToFile)
        self.receiversThreadPool.start(comms)

    def blanking(self):
        blanker = Blank()
        self.receiversThreadPool.start(blanker)


def test():
    print("Test")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())
