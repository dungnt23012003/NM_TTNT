import turtle
from pyproj import Transformer
from pyatlas.atlas import Atlas

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
turtle.tracer(0, 0)
turtle.width(3)

# Test
atlas = Atlas('phuong_thanh_cong_keep_all.atlas')

for node in atlas.nodes():
    turtle_teleport(*lat_long_2_turtle_pos(*get_node_lat_long(node)))
    turtle.goto(lat_long_2_turtle_pos(*get_node_lat_long(node)))

# Loop
turtle.update()
turtle.mainloop()
