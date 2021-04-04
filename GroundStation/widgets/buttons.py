from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

import functions

class Buttons(QWidget):

    def __init__(self, *args, **kwargs):
        super(Buttons, self).__init__(*args, **kwargs)

        layoutV = QVBoxLayout()
        layoutH1 = QHBoxLayout()
        layoutH2 = QHBoxLayout()

        b11 = QPushButton()
        b12 = QPushButton()
        b13 = QPushButton()
        b21 = QPushButton()
        b22 = QPushButton()
        b23 = QPushButton()

        b11.setText('button[1,1]')
        b12.setText('button[1,2]')
        b13.setText('button[1,3]')
        b21.setText('button[2,1]')
        b22.setText('button[2,2]')
        b23.setText('button[2,3]')



        layoutH1.addWidget(b11)
        layoutH1.addWidget(b12)
        layoutH1.addWidget(b13)

        layoutH2.addWidget(b21)
        layoutH2.addWidget(b22)
        layoutH2.addWidget(b23)

        layoutV.addLayout(layoutH1)
        layoutV.addLayout(layoutH2)

        self.setLayout(layoutV)

