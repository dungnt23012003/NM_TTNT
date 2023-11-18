import turtle

MAP_HEIGHT = 390
MAP_WIDTH = 575

LAT_1 = 21.0131
LONG_1 = 105.8040

LAT_2 = 21.0279
LONG_2 = 105.8274

screen = turtle.Screen()
screen.bgpic('map.gif')
screen.setup(2*MAP_WIDTH + 30, 2*MAP_HEIGHT + 30)

turtle.goto(MAP_WIDTH, MAP_HEIGHT)

turtle.mainloop()
