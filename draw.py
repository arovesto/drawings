import turtle
from math import cos, sin, pi


def draw(x, y):
    turtle.goto(x, y)


def move(x, y): 
    turtle.up()
    turtle.setpos(x, y)
    turtle.down()


def dot(x, y, size=5): 
    move(x, y)
    turtle.dot(size)


def dotP(a, size=5):
    return dot(a[0], a[1], size)


def drawP(a):
    return draw(a[0], a[1])


def moveP(a):
    return move(a[0], a[1])


def subP(a, b):
    return (a[0] - b[0], a[1] - b[1])


def rotateP(p, angle):
    angle = angle / 180.0 * pi
    return (p[0] * cos(angle) - p[1] * sin(angle), p[0] * sin(angle) + p[1] * cos(angle)) 


def start(width=1920, height=1280):
    turtle.setup(width, height, startx=None, starty=0)
    turtle.hideturtle()    
    turtle.tracer(0)  


def end():
    turtle.update()
    turtle.done()


def start_with_time(speed=0, width=1920, height=1280):
    turtle.setup(width, height, startx=None, starty=0)
    turtle.hideturtle()
    turtle.speed(speed)

