import tkinter as tk
from turtle import RawTurtle, TurtleScreen

from pyatlas.atlas import Atlas
from pyproj import Geod
from pyproj import Transformer

from collections import deque

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

start_x = 0
start_y = 0
start_node = atlas.nodes().__next__()

end_x = 0
end_y = 0
end_node = start_node

flag = 0


def distance(lat1, lon1, lat2, lon2):
    az12, az21, dist = wgs84_geod.inv(lon1, lat1, lon2, lat2)
    return dist


def lat_long_2_turtle_pos(lat, long):
    x, y = transformer.transform(lat, long)

    turtle_x = MAP_WIDTH * (2 * x - X_1 - X_2) / (X_2 - X_1)
    turtle_y = MAP_HEIGHT * (2 * y - Y_1 - Y_2) / (Y_2 - Y_1)

    return turtle_x, turtle_y


def turtle_pos_2_lat_long(turtle_x, turtle_y):
    x = (turtle_x * (X_2 - X_1) / MAP_WIDTH + X_1 + X_2) / 2
    y = (turtle_y * (Y_2 - Y_1) / MAP_HEIGHT + Y_1 + Y_2) / 2

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


def turtle_go_to_dotted(x, y, dot_length=10):
    pass


def on_click(event_origin):
    global flag, start_node, end_node, start_x, start_y, end_x, end_y

    print("Clicked")

    if flag == 0:
        start_x = event_origin.x - MAP_WIDTH - BORDER_SIZE
        start_y = -event_origin.y + MAP_HEIGHT - BORDER_SIZE

        start_node = get_closest_node(*turtle_pos_2_lat_long(start_x, start_y))

        turtle_teleport(start_x, start_y)
        turtle.goto(*lat_long_2_turtle_pos(*get_node_lat_long(start_node)))
        flag += 1
    elif flag == 1:
        end_x = event_origin.x - MAP_WIDTH - BORDER_SIZE
        end_y = -event_origin.y + MAP_HEIGHT - BORDER_SIZE

        end_node = get_closest_node(*turtle_pos_2_lat_long(end_x, end_y))

        # BFS Start
        visited = set()
        fringe = deque()
        parent = {}

        fringe.append(start_node)
        parent[start_node] = start_node

        # Setup Turtle
        screen.tracer(300, 0)

        while fringe:
            current_node = fringe.popleft()

            if current_node == end_node:
                break

            if current_node in visited:
                continue

            visited.add(current_node)

            turtle_teleport(*lat_long_2_turtle_pos(*get_node_lat_long(parent[current_node])))
            turtle.goto(lat_long_2_turtle_pos(*get_node_lat_long(current_node)))

            for out_edge in current_node.out_edges():
                if out_edge.end() not in visited:
                    fringe.append(out_edge.end())
                    parent[out_edge.end()] = current_node

        turtle.clear()
        current_node = end_node
        turtle_teleport(end_x, end_y)
        while parent[current_node] != current_node:
            turtle.goto(lat_long_2_turtle_pos(*get_node_lat_long(current_node)))
            current_node = parent[current_node]

        turtle.goto(lat_long_2_turtle_pos(*get_node_lat_long(current_node)))
        turtle.goto(start_x, start_y)
        # BFS End

        screen.update()
        screen.tracer(1, 0)

        turtle_teleport(end_x, end_y)
        flag += 1
    elif flag == 2:
        turtle.clear()
        flag = 0


root = tk.Tk()
root.focus()
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

# screen.mainloop()
root.mainloop()
