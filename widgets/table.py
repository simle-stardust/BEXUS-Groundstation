from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from datetime import datetime

class Table(QWidget):

    def __init__(self, *args, header_labels, max_size, **kwargs):
        super(Table, self).__init__(*args, **kwargs)

        self.layout = QVBoxLayout()

        self.maxSize = max_size

        self.table = QTableWidget()
        self.table.setColumnCount(len(header_labels))
        self.table.setHorizontalHeaderLabels(header_labels)
        self.table.verticalHeader().setVisible(False)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

    def updateGUI(self, data):
        self.table.insertRow(0)
        for i in range(len(data)):
            #self.table.setItem(0, i, QTableWidgetItem(str(data[i])))
            if i == 0: # special treatment for timestamp
                data_to_input = datetime.utcfromtimestamp(int(data[i])).strftime('%Y-%m-%d')
            elif i == 1:
                data_to_input = datetime.utcfromtimestamp(int(data[i])).strftime('%H:%M:%S')
            else:
                data_to_input = data[i]
            
            self.table.setItem(0, i, QTableWidgetItem(str(data_to_input)))

            if self.maxSize != 0 and self.table.rowCount() > self.maxSize:
                self.table.removeRow(self.table.rowCount() - 1)
