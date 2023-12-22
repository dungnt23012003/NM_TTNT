# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QPointF
from PySide6.QtCore import Qt

import queue

point1 = QPointF()
point2 = QPointF()
flag = 0

option = "on_foot"


class MapView(QtWidgets.QGraphicsView):
    def __init__(self, mapTopLeft = QtCore.QPointF(0, 0), mapBottomRight = QtCore.QPointF(0, 0), parent = None):
        super().__init__(parent)

        self.mapTopLeft = mapTopLeft
        self.mapBottomRight = mapBottomRight
        self.__process_new_point()

        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)

        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.NoAnchor)
        # self.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.NoViewportUpdate)

        self.viewBuffer = queue.Queue()

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(int(1000/480))
        # self.timer.setInterval(0)

        self.timer.start()

        self.timer.timeout.connect(self.processBuffer)

    def processBuffer(self):
        if self.viewBuffer.empty():
            self.timer.stop()
            return

        item = self.viewBuffer.get()

        if item == 0:
            self.resetInstantly()
            return

        self.addLineOnMapIntantly(*item)

    def setImage(self, filename):
        image = QtGui.QImage(filename)
        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.pixmapItem = self.scene().addPixmap(self.pixmap)
        self.pixmapItem.setScale(0.5)

    def reset(self):
        self.viewBuffer.put(0)

    def resetInstantly(self):
        self.scene().clear()
        self.pixmapItem = self.scene().addPixmap(self.pixmap)
        self.pixmapItem.setScale(0.5)

    def setTopLeft(self, point):
        self.mapTopLeft = point
        self.__process_new_point()

    def setBottomRight(self, point):
        self.mapBottomRight = point
        self.__process_new_point()

    def mapToMap(self, point):
        mapSceneRect = self.pixmapItem.sceneBoundingRect()

        mpoint = self.mapToScene(point)
        mpoint -= mapSceneRect.topLeft()

        mpoint = QtCore.QPointF(-self.dlat*mpoint.y()/mapSceneRect.height(), -self.dlong*mpoint.x()/mapSceneRect.width())
        mpoint += self.mapTopLeft

        return mpoint


    def addCircleOnMap(self, center, radius, pen = QtGui.QPen(), brush = QtGui.QBrush()):
        lcenter = self.__mapFromMapToScene(center)
        lcenter -= QtCore.QPointF(radius, radius)
        pen.setWidthF(1.5)

        return self.scene().addEllipse(lcenter.x(), lcenter.y(), 2*radius, 2*radius, pen, brush)

    def addLineOnMapIntantly(self, point_1, point_2, pen = QtGui.QPen()):
        npoint_1 = self.__mapFromMapToScene(point_1)
        npoint_2 = self.__mapFromMapToScene(point_2)
        pen.setWidthF(3)

        return self.scene().addLine(npoint_1.x(), npoint_1.y(), npoint_2.x(), npoint_2.y(), pen)

    def addLineOnMap(self, point_1, point_2, pen = QtGui.QPen()):
        self.timer.start()
        self.viewBuffer.put((point_1, point_2, pen))

    def addPointOnMap(self, point, pen = QtGui.QPen()):
        pen.setBrush(Qt.BrushStyle.SolidPattern)
        self.addCircleOnMap(point, 3, pen, QtGui.QBrush(Qt.BrushStyle.SolidPattern))

    def mousePressEvent(self, event):
        if not self.viewBuffer.empty():
            return

        import control_processes
        global point1, point2, flag

        if(flag == 0) :
            point = event.pos()
            point1 = self.mapToMap(point)

            self.resetInstantly()
            self.addPointOnMap(point1 + QPointF(0, 0))
            #print(point1.x(), point1.y())
            #point1 = control_processes.get_closest_node(point)
            #print(point01.x(), point01.y())
            #self.addCircleOnMap(point01, 10)
            #self.addLineOnMap(point, point1)
            #control_processes.change_on_map(self, point, point1)
            #self.addCircleOnMap(point01, 10)
            flag += 1
        else :
            point = event.pos()
            point2 = self.mapToMap(point)
            self.addPointOnMap(point2 + QPointF(0, 0))
            #self.addCircleOnMap(point2, 10)
            #point2 = control_processes.get_closest_node(point2)
            flag = 0
            #control_processes.draw(point1, point2)
            control_processes.A_Star_search(self, point1, point2, option)
        

    def __process_new_point(self):
        self.dlat = self.mapTopLeft.x() - self.mapBottomRight.x()
        self.dlong = self.mapTopLeft.y() - self.mapBottomRight.y()


    def __mapFromMapToScene(self, point):
        mapSceneRect = self.pixmapItem.sceneBoundingRect()
        spoint = point
        spoint -= self.mapTopLeft
        spoint = QtCore.QPointF(-mapSceneRect.width()*spoint.y()/self.dlong, -mapSceneRect.height()*spoint.x()/self.dlat)
        spoint += mapSceneRect.topLeft()

        return spoint

    def setOption(self, vehicle):
        global option
        option = vehicle

'''
from control_processes import point1, point2

point = event.pos()
point = self.mapToMap(point)
print(point.x(), point.y())
self.addCircleOnMap(point, 10)
'''

