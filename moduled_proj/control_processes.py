from itertools import count
from control_Read_osm import *
from control_distance import distance
from PySide6.QtCore import QPointF, QPoint
from models_mapview import MapView
import queue

graph = Osm(r"C:\Users\Admin\NM_TTNT\moduled_proj\models_phuongthanhcong.osm")

unique = count()

def get_closest_node(c_point) : 
    global graph
    closest_node = next(iter(graph.Nodes_have_ways.values()))
    for node in graph.Nodes_have_ways.values() :
        if( distance(node.get_lat(), node.get_lon(), c_point.x(), c_point.y()) < distance(closest_node.get_lat(), closest_node.get_lon(), c_point.x(), c_point.y())) :
            closest_node = node
    return closest_node

def A_Star_search(mapp, poi1, poi2) :
    global graph

    P = QPointF(poi1.x(), poi1.y())
    Q = QPointF(poi2.x(), poi2.y())

    start_point = get_closest_node(poi1)
    end_point = get_closest_node(poi2)

    mapp.addLineOnMap(poi1, QPointF(start_point.get_lat(), start_point.get_lon()))
    mapp.addLineOnMap(poi2, QPointF(end_point.get_lat(), end_point.get_lon()))

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
        
        for out_edge in current_node.edges :
            if out_edge.end() not in closed and out_edge.get_tag != "footway" :       # tag way?
                closed.add(out_edge.end())
                dis_from_start_to[out_edge.end()] = dis_from_start_to[current_node] + distance(current_node.get_lat(), current_node.get_lon(), (out_edge.end()).get_lat(), (out_edge.end()).get_lon())
                fringe.put((dis_from_start_to[out_edge.end()] + distance(out_edge.end().get_lat(), out_edge.end().get_lon(), end_point.get_lat(), end_point.get_lon()), out_edge.end()))
                parent[out_edge.end()] = current_node
    
    mapp.reset()
    previous_node = end_point
    current_node = parent.get(end_point)
    ep = QPointF(previous_node.get_lat(), previous_node.get_lon())
    pep = QPointF(current_node.get_lat(), current_node.get_lon())
    #mapp.addLineOnMap(ep, pep)
    mapp.addLineOnMap(ep, Q)
    print(Q.x(), Q.y())

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
    mapp.addLineOnMap(pepl, P)
    