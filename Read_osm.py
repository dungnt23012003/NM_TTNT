import xml.etree.ElementTree as ElementTree


class Node:

    __id = None
    __lat = None
    __lon = None

    def __init__(self, id, lat, lon):
        self.id = id
        self.lon = float(lon)
        self.lat = float(lat)
        self.edges = []

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_id(self):
        return self.id

    def add_edge(self, edge):
        self.edges.append(edge)


class Edge:

    __head_node = None
    __tail_node = None
    __tag = None

    def __init__(self, head_node: Node, tail_node: Node, tag_value: str):
        self.head_node = head_node
        self.tai_node = tail_node
        self.tag = tag_value

    def start(self):
        return self.head_node

    def end(self):
        return self.tai_node

    def get_tag(self):
        return self.tag


class Osm:

    Nodes = {}                                                          # tập node

    def __init__(self, map_osm_file_path):
        mydata = ElementTree.parse(map_osm_file_path)
        my_node = {}
        for item in mydata.iterfind('node'):                            # tìm các item trong tập lớn có tên là node
            my_node[item.attrib['id']] = Node(item.attrib['id'], item.attrib['lat'], item.attrib['lon'])

        # for node in my_node.values():
        #     print(node.get_id() + ' ' + str(node.get_lat()) + ' ' + str(node.get_lon()))

        for item in mydata.iterfind('way'):                             #tìm các item có tên way trong mỗi item m
            # print('way: ' + item.attrib['id'])
            node_in_way = []                                            #tập các node trên 1 đường
            flag_is_way = False
            flag_is_oneway = False
            flag_is_footway = False
                                                                        #?? tag, item, attribute là cái gì
            for tag in item.iterfind('tag'):                            #tìm các item có tên tag trong mỗi item
                if tag.attrib['k'] == 'highway':
                    flag_is_way = True
                if tag.attrib['k'] == 'oneway' and tag.attrib['v'] == 'yes':
                    flag_is_oneway = True
                if tag.attrib['k'] == 'highway' and tag.attrib['v'] == 'footway':
                    flag_is_footway = True

            if flag_is_way is True:
                if flag_is_footway is True:
                    for node in item.iterfind('nd'):
                        node_in_way.append(node.attrib['ref'])
                    for index in range(0, len(node_in_way) - 1):
                        my_node[node_in_way[index]].add_edge(
                            Edge(my_node[node_in_way[index]], my_node[node_in_way[index + 1]], 'footway'))
                        my_node[node_in_way[index + 1]].add_edge(
                            Edge(my_node[node_in_way[index + 1]], my_node[node_in_way[index]], 'footway'))
                else:
                    if flag_is_oneway is True:
                        for node in item.iterfind('nd'):
                            node_in_way.append(node.attrib['ref'])
                        for index in range(0, len(node_in_way) - 1):
                            my_node[node_in_way[index]].add_edge(
                                Edge(my_node[node_in_way[index]], my_node[node_in_way[index + 1]], 'oneway'))
                    else:
                        for node in item.iterfind('nd'):
                            node_in_way.append(node.attrib['ref'])
                        for index in range(0, len(node_in_way) - 1):
                            my_node[node_in_way[index]].add_edge(
                                Edge(my_node[node_in_way[index]], my_node[node_in_way[index + 1]], ''))
                            my_node[node_in_way[index + 1]].add_edge(
                                Edge(my_node[node_in_way[index + 1]], my_node[node_in_way[index]], ''))

        self.Nodes = my_node

    def print_all_node(self):
        for node in self.Nodes.values():
            print('node ' + node.get_id())
            for nei in node.edges:
                print(nei.end().get_id() + ' tag: ' + nei.get_tag())
