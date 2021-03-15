from PyQt5 import QtGui
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QTabWidget, QScrollArea
from widgets.display import Display
from widgets.table import Table
from widgets.charts import Charts
from pyqtgraph.console import ConsoleWidget
from widgets.buttons import Buttons

from threads.tester import Tester
from threads.UDPlistener import UDPListener

import hjson
from datetime import date
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Stardust Ground Station")
        self.setWindowIcon(QtGui.QIcon('stardust.ico'))
        self.resize(1000,600)

        self.logFile = 'logs/StardustGroundstation' + str(date.today()) + '.txt'

        with open("config.hjson", "r") as file:
            config = hjson.load(file)

        self.layout = QVBoxLayout()

        self.display = Display(structure=config['structure'], units=config['units'], phases=config['phases'])
        self.tabs = QTabWidget()

        self.updatableWidgets = []

        self.layout.addWidget(self.display)
        self.updatableWidgets.append(self.display)
        self.layout.addWidget(self.tabs)

        if config['table']:
            self.table = Table(headerLabels=config['labels'], maxSize=config['maxSize'])
            self.updatableWidgets.append(self.table)
            self.tabs.addTab(self.table, 'Table')
        if config['charts']:
            self.charts = Charts(structure=config['structure'], units=config['units'])
            self.updatableWidgets.append(self.charts)
            self.scrollCharts = QScrollArea()
            self.scrollCharts.setWidgetResizable(True)
            self.scrollCharts.setWidget(self.charts)
            self.tabs.addTab(self.scrollCharts, 'Charts')
        if config['console']:
            self.console = ConsoleWidget()
            self.tabs.addTab(ConsoleWidget(), 'Console')
        if config['buttons']:
            self.buttons = Buttons()
            self.tabs.addTab(self.buttons, 'Function Buttons')

        del config

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.testDataRandom = []

        self.threadpool = QThreadPool()

        self.testing()


    def update(self, input):
        for widget in self.updatableWidgets:
            widget.update(input)

    def printToFile(self, input):
        file = open(self.logFile, 'a+')
        file.write(input)
        file.close()

    def testing(self):
        tester = Tester(self)
        tester.signals.result.connect(self.update)
        self.threadpool.start(tester)

    def listening(self):
        listener = UDPListener(self)
        listener.signals.list.connect(self.update)
        listener.signals.string.connect(self.printToFile)
        self.threadpool.start(listener)

def test():
    print("Test")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())
