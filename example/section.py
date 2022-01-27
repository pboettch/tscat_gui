from PySide2 import QtCore, QtWidgets

from tscat_gui.utils.section import Section

import sys


class Section1(Section):
    def __init__(self, parent=None):
        super().__init__("Section", 100, parent)

        anyLayout = QtWidgets.QVBoxLayout()
        anyLayout.addWidget(QtWidgets.QLabel("Some Text in Section", self))
        anyLayout.addWidget(QtWidgets.QPushButton("Button in Section", self))

        self.setContentLayout(anyLayout)


class Section2(Section):
    def __init__(self, parent=None):
        super().__init__("Section", 100, parent)

        anyLayout = QtWidgets.QVBoxLayout()
        anyLayout.addWidget(QtWidgets.QLabel("Some Text in Section", self))
        anyLayout.addWidget(QtWidgets.QPushButton("Button in Section", self))
        anyLayout.addWidget(QtWidgets.QLabel("Some Text in Section", self))
        anyLayout.addWidget(QtWidgets.QPushButton("Button in Section", self))
        anyLayout.addWidget(QtWidgets.QPushButton("Button in Section", self))
        anyLayout.addWidget(QtWidgets.QPushButton("Button in Section", self))
        anyLayout.addWidget(QtWidgets.QPushButton("Button in Section", self))
        anyLayout.addWidget(QtWidgets.QPushButton("Button in Section", self))
        anyLayout.addWidget(QtWidgets.QPushButton("Button in Section", self))

        self.setContentLayout(anyLayout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QMainWindow()

    w = QtWidgets.QWidget()

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(Section1())
    layout.addWidget(Section2())
    layout.addStretch()
    w.setLayout(layout)

    main.setCentralWidget(w)
    main.show()

    sys.exit(app.exec_())
