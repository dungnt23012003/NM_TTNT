# This Python file uses the following encoding: utf-8
import sys
from PySide6 import QtCore, QtWidgets, QtGui, QtSvgWidgets
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt 

from models_mapview import MapView

map = MapView

def changeViewZoom(value):
    window.mapView.setTransform(QtGui.QTransform.fromScale(value/100, value/100))


QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

if __name__ == "__main__":
    
    app = QApplication([])
    # ui_file = QtCore.QFile(r"C:\Users\Tuand\PycharmProjects\NM_TTNT\moduled_proj\views_mainwindow.ui")
    ui_file = QtCore.QFile(r"C:\Users\Admin\NM_TTNT\moduled_proj\views_mainwindow.ui")
    # ui_file = QtCore.QFile(r"views_mainwindow.ui")

    ui_file.open(QtCore.QFile.ReadOnly)

    loader = QUiLoader()
    loader.registerCustomWidget(map)

    window = loader.load(ui_file)
    # window.mapView.setImage(r"C:\Users\Tuand\PycharmProjects\NM_TTNT\moduled_proj\models_map.png")
    window.mapView.setImage(r"C:\Users\Admin\NM_TTNT\moduled_proj\models_map.png")
    #window.mapView.setImage(r"models_map.png")

    window.mapView.setTopLeft(QtCore.QPointF(21.02761, 105.80665))
    window.mapView.setBottomRight(QtCore.QPointF(21.01390, 105.82438))

    window.slider.valueChanged.connect(changeViewZoom)
    window.footButton.clicked.connect(lambda: window.mapView.setOption("on_foot"))
    window.carButton.clicked.connect(lambda: window.mapView.setOption("by_car"))

    def setLineColor():
        window.mapView.setStartColor(QtGui.QColor(int(window.startColor.text(), 16)))
        window.mapView.setEndColor(QtGui.QColor(int(window.endColor.text(), 16)))
        window.mapView.setInitialDuration(int(window.initialDuration.text()))
        window.mapView.setDurationStep(int(window.durationStep.text()))
    window.setColorButton.pressed.connect(setLineColor)

    window.rateButton.pressed.connect(lambda: window.mapView.setLineRate(int(window.lineRate.text())))

    setLineColor()

    window.show()

    sys.exit(app.exec())
