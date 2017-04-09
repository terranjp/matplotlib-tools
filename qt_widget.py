import math

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as MPLtoolbar)
from matplotlib.figure import Figure

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


toolTipStyle = """
    QLabel{
    background-color: black ;
    color: white;
    padding: 5px;
    border-radius: 5px;
    }

"""


class PlotWindow(QWidget):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)

        changeButton = QPushButton("Change")
        changeButton.pressed.connect(self.changePlot)
        changeSizeBtn = QPushButton("changeSize")

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        toolWidget = QWidget()
        toolWidget.setMaximumHeight(48)
        toolLayout = QHBoxLayout()
        toolLayout.setContentsMargins(0, 0, 0, 0)
        toolWidget.setLayout(toolLayout)

        self.ax = None
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.MPL_toolbar = MPLtoolbar(self.canvas, self, coordinates=True)

        self.toScaleButton = QPushButton('To Scale')

        mainLayout.addWidget(self.canvas)
        toolLayout.addWidget(self.MPL_toolbar)
        toolLayout.addWidget(self.toScaleButton)
        mainLayout.addWidget(toolWidget)
        mainLayout.addWidget(changeButton)
        mainLayout.addWidget(changeSizeBtn)

        self.tooltipWidget = QLabel('Test')
        self.tooltipWidget.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.tooltipWidget.setStyleSheet(toolTipStyle)

        self.ruler = Ruler(fig=self.fig)
        self.rulerCheckbox = QCheckBox()
        self.rulerCheckbox.setText("Ruler On:")
        toolLayout.addWidget(self.rulerCheckbox)
        self.rulerCheckbox.stateChanged.connect(self.handleRulerCheck)
        self.handleRulerCheck()

    def handleRulerCheck(self):
        if self.rulerCheckbox.isChecked() == True:
            self.ruler.rulerActivated = True
        else:
            self.ruler.rulerActivated = False

    def plotCoords(self, coords):

        # Clear the figure
        self.fig.clf()
        # Setup the base plot
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Horizontal Distance (ft)')
        self.ax.set_ylabel('Vertical Distance (ft)')
        self.ax.grid(True)
        self.ax.set_xlabel('Horizontal Distance (ft)')
        self.ax.set_ylabel('Vertical Distance (ft)')
        # Plot seabed
        self.ax.plot(coords.x, coords.y)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onPlotHover)
        self.canvas.draw()

    def findNearest(self, array, value):
        idx = (np.abs(array - value)).argmin()
        return idx

    @staticmethod
    def findNearestFast(array, value):
        idx = np.searchsorted(array, value, side="left")
        if idx > 0 and (idx == len(array) or math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx])):
            return array[idx - 1]
        else:
            return array[idx]

    def onPlotHover(self, event):
        for curve in self.ax.get_lines():
            if curve.contains(event)[0]:
                print(event)
                xCoord = event.xdata
                index = int(self.findNearestFast(self.output.lineCoords.x, xCoord))
                # print('Index: ', index)
                tensionString = 'xTension: {:0.2f} kips; yTension: {:0.2f} kips'.format(self.output.lineTension.x[index], self.output.lineTension.y[index])
                self.tooltipWidget.setText(tensionString)
                tooltipPos = QPoint(QCursor.pos().x() + 10, QCursor.pos().y() - 10)

                self.tooltipWidget.move(tooltipPos)
                self.tooltipWidget.show()
            # else:
                # self.tooltipWidget.hide()
                # print('hide')

    # def onMouseEnter(self, event):
    #     print('Enter figure')
    #
    # def onMouseLeave(self, event):
    #     self.tooltipWidget.hide()




        # self.fig.tight_layout()
        self.canvas.draw()

    def changePlot(self):
        pass
        # self.PlotOnFigure(cat.catOutput)