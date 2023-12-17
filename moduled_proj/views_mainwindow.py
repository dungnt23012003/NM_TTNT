# This Python file uses the following encoding: utf-8
import sys
from PySide6 import QtCore, QtWidgets, QtGui, QtSvgWidgets
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt 

from models_mapview import MapView

map = MapView

def changeViewZoom(value):
    window.mapView.setTransform(QtGui.QTransform.fromScale(value/50, value/50))
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

if __name__ == "__main__":
    
    app = QApplication([])

    ui_file = QtCore.QFile(r"C:\Users\Admin\NM_TTNT\moduled_proj\views_mainwindow.ui")
    ui_file.open(QtCore.QFile.ReadOnly)

    loader = QUiLoader()
    loader.registerCustomWidget(map)

    window = loader.load(ui_file)

    window.mapView.setImage(r"C:\Users\Admin\NM_TTNT\moduled_proj\models_map.png")
    window.mapView.setTopLeft(QtCore.QPointF(21.02761, 105.80665))
    window.mapView.setBottomRight(QtCore.QPointF(21.01390, 105.82438))

    window.mapView.addCircleOnMap(QtCore.QPointF(21.0167680, 105.8149337), 10)

    window.slider.valueChanged.connect(changeViewZoom)

    window.show()


    sys.exit(app.exec())
