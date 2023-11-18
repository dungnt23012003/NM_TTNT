import tkinter as tk
from turtle import RawTurtle, TurtleScreen

from pyatlas.atlas import Atlas
from pyproj import Geod
from pyproj import Transformer

BORDER_SIZE = 4

MAP_HEIGHT = 390
MAP_WIDTH = 575

LAT_1 = 21.0131
LONG_1 = 105.8040

LAT_2 = 21.0279
LONG_2 = 105.8274

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857")
inverse_transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")
wgs84_geod = Geod(ellps='WGS84')

atlas = Atlas('phuong_thanh_cong.atlas')

X_1, Y_1 = transformer.transform(LAT_1, LONG_1)
X_2, Y_2 = transformer.transform(LAT_2, LONG_2)


def distance(lat1, lon1, lat2, lon2):
    az12, az21, dist = wgs84_geod.inv(lon1, lat1, lon2, lat2)
    return dist


def lat_long_2_turtle_pos(lat, long):
    x, y = transformer.transform(lat, long)

    turtle_x = MAP_WIDTH*(2*x - X_1 - X_2)/(X_2 - X_1)
    turtle_y = MAP_HEIGHT*(2*y - Y_1 - Y_2)/(Y_2 - Y_1)

    return turtle_x, turtle_y


def turtle_pos_2_lat_long(turtle_x, turtle_y):
    x = (turtle_x*(X_2 - X_1)/MAP_WIDTH + X_1 + X_2)/2
    y = (turtle_y*(Y_2 - Y_1)/MAP_HEIGHT + Y_1 + Y_2)/2

    return inverse_transformer.transform(x, y)


def get_node_lat_long(node):
    return node.as_location().get_latitude_deg(), node.as_location().get_longitude_deg()


def get_closest_node(lat, long):
    closest_node = atlas.nodes().__next__()
    for node in atlas.nodes():
        if distance(lat, long, *get_node_lat_long(node)) < distance(lat, long, *get_node_lat_long(closest_node)):
            closest_node = node

    return closest_node


def turtle_teleport(x, y):
    turtle.up()
    turtle.ht()
    turtle.goto(x, y)
    turtle.st()
    turtle.down()


def on_click(event_origin):
    turtle.width(3)
    screen.tracer(0, 0)

    print(event_origin.x, event_origin.y)
    x = event_origin.x - MAP_WIDTH - BORDER_SIZE
    y = -event_origin.y + MAP_HEIGHT - BORDER_SIZE

    turtle_teleport(x, y)
    turtle.goto(x, y)

    lat, long = turtle_pos_2_lat_long(x, y)
    print(lat, long)

    step = (LONG_2 - LONG_1)/20
    x = LONG_1
    turtle_teleport(*lat_long_2_turtle_pos(lat, x))

    for i in range(20):
        turtle_teleport(*lat_long_2_turtle_pos(lat, x))
        turtle.goto(*lat_long_2_turtle_pos(lat, x))
        x += step
        print(x, long)

    screen.update()
    print("Done.")


root = tk.Tk()
root.bind("<Button 1>", on_click)

canvas2 = tk.Canvas(root, width=1151, height=781)
canvas2.pack()

screen = TurtleScreen(canvas2)
screen.bgpic('map.gif')
turtle = RawTurtle(screen)

# Test
print(lat_long_2_turtle_pos(*turtle_pos_2_lat_long(30, 300)))

# Turtle setup
turtle.speed(0)
# screen.tracer(5, 0)
screen.mainloop()
