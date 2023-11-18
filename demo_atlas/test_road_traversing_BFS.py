import turtle
from pyproj import Transformer
from pyatlas.atlas import Atlas
from collections import deque

MAP_HEIGHT = 390
MAP_WIDTH = 575

LAT_1 = 21.0131
LONG_1 = 105.8040

LAT_2 = 21.0279
LONG_2 = 105.8274

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857")

X_1, Y_1 = transformer.transform(LAT_1, LONG_1)
X_2, Y_2 = transformer.transform(LAT_2, LONG_2)


def lat_long_2_turtle_pos(lat, long):
    x, y = transformer.transform(lat, long)

    turtle_x = MAP_WIDTH*(2*x - X_1 - X_2)/(X_2 - X_1)
    turtle_y = MAP_HEIGHT*(2*y - Y_1 - Y_2)/(Y_2 - Y_1)

    return turtle_x, turtle_y


def turtle_teleport(x, y):
    turtle.up()
    turtle.ht()
    turtle.goto(x, y)
    turtle.st()
    turtle.down()


def get_node_lat_long(node):
    return node.as_location().get_latitude_deg(), node.as_location().get_longitude_deg()


def turtle_teleport_node(node):
    turtle_teleport(*lat_long_2_turtle_pos(node.as_location().get_latitude_deg(), node.as_location().get_longtitude_deg()))


# Setup turtle
screen = turtle.Screen()
screen.bgpic('map.gif')
screen.setup(2*MAP_WIDTH + 30, 2*MAP_HEIGHT + 30)
turtle.speed(0)
turtle.tracer(100, 0)

# Test
atlas = Atlas('phuong_thanh_cong.atlas')
visited = set()
fringe = deque()
parent = {}

current_node = atlas.node(8273495790000000)
fringe.append(current_node)
parent[current_node] = current_node

while fringe:
    current_node = fringe.popleft()

    turtle_teleport(*lat_long_2_turtle_pos(*get_node_lat_long(parent[current_node])))
    turtle.goto(lat_long_2_turtle_pos(*get_node_lat_long(current_node)))

    # Debug print
    print(len(visited), len(fringe), len(parent))

    for out_edge in current_node.out_edges():
        if out_edge.get_highway_tag_value() is not None and out_edge.get_highway_tag_value() != 'footway' and out_edge.end() not in visited:
            print(out_edge.get_highway_tag_value())
            visited.add(out_edge.end())
            fringe.append(out_edge.end())
            parent[out_edge.end()] = current_node

turtle_teleport(*lat_long_2_turtle_pos(*get_node_lat_long(current_node)))

# Loop
turtle.mainloop()
