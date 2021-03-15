from PyQt5.QtWidgets import QWidget, QVBoxLayout
from pyqtgraph.console import ConsoleWidget


class Console(QWidget):

    def __init__(self, *args, **kwargs):
        super(Console, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()

        layout.addWidget(ConsoleWidget)

        self.setLayout(layout)