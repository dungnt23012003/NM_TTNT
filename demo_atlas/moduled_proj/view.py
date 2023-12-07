import tkinter as tk;
import turtle

from controll import click_to_coor
import module

MAP_WIDTH, MAP_HEIGHT = (module.WIDTH, module.HEIGHT)

root = tk.Tk()
root.focus()

#using ScrolledCanvas because sometime the map.gif size is bigger than the canvas size

sCanvas = turtle.ScrolledCanvas(root, width = MAP_WIDTH, height=MAP_HEIGHT, canvwidth=MAP_WIDTH, canvheight=MAP_HEIGHT)
sCanvas.pack()

screen = turtle.TurtleScreen(sCanvas)
screen.bgpic(r"C:\Users\Admin\NM_TTNT\demo_atlas\map.gif")
mainTurtle = turtle.RawTurtle(screen)

screen.onscreenclick(click_to_coor)         #using screen.onscreenclick so when the scrollbar change, the O-oringinal not change.

root.mainloop()








