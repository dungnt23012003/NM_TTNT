from PySide6 import QtWidgets, QtGui, QtCore

class FadingGraphicsLineItem(QtCore.QObject, QtWidgets.QGraphicsLineItem):
    colorChanged = QtCore.Signal(QtGui.QColor)

    def __init__(self, startColor, endColor, duration, pen=QtGui.QPen()):
        QtCore.QObject.__init__(self)
        QtWidgets.QGraphicsLineItem.__init__(self)

        self.pen = pen

        self.anim = QtCore.QPropertyAnimation(self, b"color")
        self.anim.setStartValue(startColor)
        self.anim.setEndValue(endColor)
        self.anim.setDuration(duration)

        self.anim.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def setColor(self, color):
        self.pen.setColor(color)
        self.setPen(self.pen)
        self.colorChanged.emit(color)

    def color(self):
        return self.pen.color()

    color = QtCore.Property(QtGui.QColor, color, setColor)
