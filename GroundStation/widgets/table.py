from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout


class Table(QWidget):


    def __init__(self, *args, headerLabels, maxSize, **kwargs):
        super(Table, self).__init__(*args, **kwargs)

        self.layout = QVBoxLayout()

        self.maxSize = maxSize

        self.table = QTableWidget()
        self.table.setColumnCount(len(headerLabels))
        self.table.setHorizontalHeaderLabels(headerLabels)
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def update(self, input):
        self.table.insertRow(0)
        for i in range(len(input)):
            self.table.setItem(0, i, QTableWidgetItem(str(input[i])))
            if self.maxSize != 0 and self.table.rowCount() > self.maxSize:
                self.table.removeRow(self.table.rowCount()-1)