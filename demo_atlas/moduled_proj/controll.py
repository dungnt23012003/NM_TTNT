import module
from PIL import Image


start_x_turtle, start_y_turtle = 0, 0
end_x_turtle, end_y_turtle = 0, 0
flag = 0                                    # tag to the start: 0, to the end: 1




#------------------------------------------------------------------------------------------------------------------
# to get turtle-coordinations of one click
def click_to_coor(x, y) :

    from view import mainTurtle                 # internal import to avoid circular import

    global start_x_turtle, start_y_turtle
    global end_x_turtle, end_y_turtle
    global flag

    if(flag==0) :
        start_x_turtle, start_y_turtle = (x, y)
        mainTurtle.goto(x, y)

    if(flag==1) :
        end_x_turtle, end_y_turtle = (x, y)
        mainTurtle.goto(x, y)

    outong()   
    flag += 1
    if(flag == 2) : flag = 0
#------------------------------------------------------------------------------------------------------------------
# test connection
def outong() :
    global start_x_turtle, start_y_turtle
    global end_x_turtle, end_y_turtle
    global flag
    if(flag==0) : print(start_x_turtle, start_y_turtle)
    if(flag==1) : print(end_x_turtle, end_y_turtle)