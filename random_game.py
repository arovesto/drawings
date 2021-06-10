import random
from math import sin, pi, cos

from draw import start, end, dotP, rotateP, start_with_time


def find_right_polygon(Vertexes, radius, center = (0, 0)):
    return [(int(center[0] + radius * sin(2 * pi / Vertexes * n)), int(center[1] - radius * cos(2 * pi / Vertexes * n))) 
    for n in range(Vertexes)]


def new_point(a, b, k = 2, m = 1, z = 1): return ((m * b[0] + z * a[0]) / k, (m * b[1] + z * a[1]) / k)


#need to rotate around point
def gen_centers(firstp, grid, vertexes, radius):
    xcoordstep = radius * cos((pi - 2 * pi / Vertexes) / 2)
    ycoordstep = radius * sin((pi - 2 * pi / Vertexes) / 2)
    xzero = firstp[0]
    yzero = firstp[1]
    rotation = 1
    centers = []
    for x in range(grid[0]):
        for y in range(grid[1]):
            centers.append(((xzero, yzero), rotation))
            yzero += ycoordstep
            rotation = (rotation + 1) % 2
        xzero += xcoordstep
        rotation = (rotation + 1) % 2
    for c in centers: print(c)
    return centers

'''
Vertexes = number of Vertexes
next = (prev * MultForPrevious + random vertex * MultForVertex) / Divisor
withMultForPreviousedium = include medium points between Vertexes
==========================================================================================
Triangle Vertexes = 3 Divisor = 2 MultForPrevious = 1 MultForVertex = 1 withMedium = False
Square Vertexes = 4 Divisor = 3 MultForPrevious = 2 MultForVertex = 1 withMedium = True
Sixangler Vertexes = 6 Divisor = 3 MultForPrevious = 2 MultForVertex = 1 withMedium = False
'''
Vertexes = 3
Divisor = 2
MultForPrevious = 1
MultForVertex = 1
withMedium = False

zoom = 0
rotate = 180
ignore_first = 10
polygon_radius = 500 * (zoom + 1)
number_of_dots = 10000
start_point = (0, 0)
dot_size = 3
big_dot_size = 10


Centers = gen_centers((-500, -250), (3, 2), Vertexes, polygon_radius)

Points = [rotateP(p, rotate) for p in find_right_polygon(Vertexes, polygon_radius, (290 * zoom, 0 * zoom))]
MovedPoints = Points[1:]
MovedPoints.append(Points[0])
MiddlePoints = [new_point(Points[i], MovedPoints[i]) for i in range(len(Points))]
if withMedium: Points += MiddlePoints

start_with_time()  # start() for instant drawing
for p in Points: dotP(p, big_dot_size)
for _ in range(number_of_dots):
    if _ not in range(ignore_first): dotP(start_point, dot_size)
    start_point = new_point(start_point, random.choice(Points), Divisor, MultForPrevious, MultForVertex)
    
end()
