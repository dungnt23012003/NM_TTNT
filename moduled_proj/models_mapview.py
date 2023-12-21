# This Python file uses the following encoding: utf-8
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QPointF

point1 = QPointF()
point2 = QPointF()
flag = 0

option = "by_car"

class MapView(QtWidgets.QGraphicsView):
    def __init__(self, mapTopLeft = QtCore.QPointF(0, 0), mapBottomRight = QtCore.QPointF(0, 0), parent = None):
        super().__init__(parent)

        self.mapTopLeft = mapTopLeft
        self.mapBottomRight = mapBottomRight
        self.__process_new_point()

        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)

    def setImage(self, filename):
        image = QtGui.QImage(filename)
        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.pixmapItem = self.scene().addPixmap(self.pixmap)
        self.pixmapItem.setScale(0.5)

    def reset(self):
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


    def addCircleOnMap(self, center, radius, pen = QtGui.QPen()):
        lcenter = self.__mapFromMapToScene(center)
        lcenter -= QtCore.QPointF(radius, radius)
        pen.setWidthF(1.5)

        return self.scene().addEllipse(lcenter.x(), lcenter.y(), 2*radius, 2*radius, pen)


    def addLineOnMap(self, point_1, point_2, pen = QtGui.QPen()):
        npoint_1 = self.__mapFromMapToScene(point_1)
        npoint_2 = self.__mapFromMapToScene(point_2)
        pen.setWidthF(3)

        return self.scene().addLine(npoint_1.x(), npoint_1.y(), npoint_2.x(), npoint_2.y(), pen)

    def mousePressEvent(self, event):
        import control_processes
        global point1, point2, flag

        if(flag == 0) :
            point = event.pos()
            point1 = self.mapToMap(point)
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


'''
from control_processes import point1, point2

point = event.pos()
point = self.mapToMap(point)
print(point.x(), point.y())
self.addCircleOnMap(point, 10)
'''

