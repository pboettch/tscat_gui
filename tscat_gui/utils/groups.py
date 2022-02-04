"""
    Elypson/qt-collapsible-section
    (c) 2016 Michael A. Voelkel - michael.alexander.voelkel@gmail.com

    This file is part of Elypson/qt-collapsible section.

    Elypson/qt-collapsible-section is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License, or
    (at your option) any later version.

    Elypson/qt-collapsible-section is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Elypson/qt-collapsible-section. If not, see <http:#www.gnu.org/licenses/>.
"""

from PySide2 import QtCore, QtWidgets


class CollapsableGroup(QtWidgets.QWidget):
    def __init__(self,
                 title: str = "",
                 animation_duration: int = 100,
                 parent=None):
        super().__init__(parent)

        self.animationDuration = animation_duration
        self.toggleButton = QtWidgets.QToolButton(self)
        self.headerLine = QtWidgets.QFrame(self)
        self.toggleAnimation = QtCore.QParallelAnimationGroup(self)
        self.contentArea = QtWidgets.QScrollArea(self)
        self.mainLayout = QtWidgets.QGridLayout(self)
        # self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        self.toggleButton.setStyleSheet("QToolButton {border: none;}")
        self.toggleButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggleButton.setArrowType(QtCore.Qt.RightArrow)
        self.toggleButton.setText(title)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(False)

        self.headerLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.headerLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.headerLine.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)

        self.contentArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)

        # let the entire widget grow and shrink with its content
        self.toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        self.toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        self.toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self.contentArea, b"maximumHeight"))

        self.mainLayout.setVerticalSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(self.toggleButton, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.mainLayout.addWidget(self.headerLine, 0, 2, 1, 1)
        self.mainLayout.addWidget(self.contentArea, 1, 0, 1, 3)
        self.setLayout(self.mainLayout)

        self.toggleButton.toggled.connect(self.toggle)

    def setContentLayout(self, contentLayout: QtWidgets.QLayout, collapsed: bool = True):
        layout = self.contentArea.layout()
        if layout:
            layout.deleteLater()

        self.contentArea.setLayout(contentLayout)

        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()

        for i in range(0, self.toggleAnimation.animationCount() - 1):
            sectionAnimation = self.toggleAnimation.animationAt(i)
            sectionAnimation.setDuration(self.animationDuration)
            sectionAnimation.setStartValue(collapsedHeight)
            sectionAnimation.setEndValue(collapsedHeight + contentHeight)

        contentAnimation = self.toggleAnimation.animationAt(self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

        self.toggleButton.setChecked(not collapsed)

    def toggle(self, collapsed):
        if collapsed:
            self.toggleButton.setArrowType(QtCore.Qt.DownArrow)
            self.toggleAnimation.setDirection(QtCore.QAbstractAnimation.Forward)
        else:
            self.toggleButton.setArrowType(QtCore.Qt.RightArrow)
            self.toggleAnimation.setDirection(QtCore.QAbstractAnimation.Backward)
        self.toggleAnimation.start()
