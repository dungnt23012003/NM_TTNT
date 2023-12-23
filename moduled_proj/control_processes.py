import time
from itertools import count
from control_Read_osm import *
from control_distance import distance
from PySide6.QtCore import QPointF, QPoint
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt

from models_mapview import MapView
import queue

# graph = Osm(r"C:\Users\Tuand\PycharmProjects\NM_TTNT\moduled_proj\models_phuongthanhcong.osm")
# graph = Osm(r"C:\Users\Admin\NM_TTNT\moduled_proj\models_phuongthanhcong.osm")
graph = Osm(r"models_phuongthanhcong.osm")

unique = count()


def check_base_on_option(tag_check, option):
    if option == "on_foot":
        if tag_check == "residential" or tag_check == "service" or tag_check == "footway" or tag_check == "tertiary":
            return True
        else:
            return False
    elif option == "by_car":
        if tag_check == "primary" or tag_check == "secondary" or tag_check == "tertiary" or tag_check == "primary_link" or tag_check == "secondary_link" or tag_check == "tertiary_link" or tag_check == "residential" or tag_check == "service":
            return True
        else:
            return False


def get_closest_node(c_point, option):
    global graph
    flag_have_found = False
    for node in graph.Nodes_have_ways.values():
        if not flag_have_found:
            for edge in node.edges:
                if check_base_on_option(edge.get_tag(), option):
                    closest_node = edge.end()
                    flag_have_found = True
                    break

    close = set()
    close.add(closest_node)
    for node in graph.Nodes_have_ways.values():
        for edge in node.edges:
            if edge.end() not in close:
                if check_base_on_option(edge.get_tag(), option):
                    if (distance(node.get_lat(), node.get_lon(), c_point.x(), c_point.y()) < distance(closest_node.get_lat(), closest_node.get_lon(), c_point.x(), c_point.y())):
                        closest_node = node
                close.add(edge.end())

    return closest_node


def A_Star_search(mapp, poi1, poi2, option):
    global graph

    P = QPointF(poi1.x(), poi1.y())
    Q = QPointF(poi2.x(), poi2.y())

    start_point = get_closest_node(poi1, option)
    end_point = get_closest_node(poi2, option)

    pen = QPen()
    pen.setStyle(Qt.PenStyle.DotLine)
    mapp.addLineOnMap(poi1, QPointF(start_point.get_lat(), start_point.get_lon()), pen)
    # mapp.addLineOnMap(poi2, QPointF(end_point.get_lat(), end_point.get_lon()))

    closed = set()
    fringe = queue.PriorityQueue()
    parent = {}
    dis_from_start_to = {start_point: 0}

    fringe.put((distance(start_point.get_lat(), start_point.get_lon(), end_point.get_lat(), end_point.get_lon()), start_point))
    parent[start_point] = start_point
    closed.add(start_point)

    while not fringe.empty() :
        current_node = fringe.get()[1]

        cur_point = QPointF(current_node.get_lat(), current_node.get_lon())
        parcur_point = QPointF(parent[current_node].get_lat(), parent[current_node].get_lon())

         # add line to cur node:
        mapp.addLineOnMap(parcur_point, cur_point)

        if current_node.get_id() == end_point.get_id() :
            break

        for out_edge in current_node.edges:
            if out_edge.end() not in closed and check_base_on_option(out_edge.get_tag(), option):       # tag way?
                closed.add(out_edge.end())
                dis_from_start_to[out_edge.end()] = dis_from_start_to[current_node] + distance(current_node.get_lat(), current_node.get_lon(), (out_edge.end()).get_lat(), (out_edge.end()).get_lon())
                fringe.put((dis_from_start_to[out_edge.end()] + distance(out_edge.end().get_lat(), out_edge.end().get_lon(), end_point.get_lat(), end_point.get_lon()), out_edge.end()))
                parent[out_edge.end()] = current_node
                print(out_edge.get_tag())
    
    mapp.reset()
    previous_node = end_point
    current_node = parent.get(end_point)
    ep = QPointF(previous_node.get_lat(), previous_node.get_lon())
    pep = QPointF(current_node.get_lat(), current_node.get_lon())
    #mapp.addLineOnMap(ep, pep)
    # mapp.addLineOnMap(ep, Q)
    print(Q.x(), Q.y())

    mapp.addLineOnMap(poi2, QPointF(end_point.get_lat(), end_point.get_lon()), pen)

    while parent.get(current_node) != current_node :
        ep = QPointF(previous_node.get_lat(), previous_node.get_lon())
        pep = QPointF(current_node.get_lat(), current_node.get_lon())
        mapp.addLineOnMap(ep, pep)
        previous_node = current_node
        current_node = parent.get(current_node)
    
    ep = QPointF(previous_node.get_lat(), previous_node.get_lon())
    pep = QPointF(current_node.get_lat(), current_node.get_lon())
    mapp.addLineOnMap(ep, pep)

    pepl = QPointF(current_node.get_lat(), current_node.get_lon())
    mapp.addLineOnMap(pepl, P, pen)
    