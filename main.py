from tkinter import *
from itertools import *
from math import *

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def findCircle(tri):
    global points

    x1, y1 = points[tri[0]]
    x2, y2 = points[tri[1]]
    x3, y3 = points[tri[2]]

    x12 = x1 - x2;
    x13 = x1 - x3;

    y12 = y1 - y2;
    y13 = y1 - y3;

    y31 = y3 - y1;
    y21 = y2 - y1;

    x31 = x3 - x1;
    x21 = x2 - x1;

    # x1^2 - x3^2
    sx13 = pow(x1, 2) - pow(x3, 2);

    # y1^2 - y3^2
    sy13 = pow(y1, 2) - pow(y3, 2);

    sx21 = pow(x2, 2) - pow(x1, 2);
    sy21 = pow(y2, 2) - pow(y1, 2);

    f = (((sx13) * (x12) + (sy13) *
        (x12) + (sx21) * (x13) +
        (sy21) * (x13)) // (2 *
        ((y31) * (x12) - (y21) * (x13))));

    g = (((sx13) * (y12) + (sy13) * (y12) +
        (sx21) * (y13) + (sy21) * (y13)) //
        (2 * ((x31) * (y12) - (x21) * (y13))));

    c = (-pow(x1, 2) - pow(y1, 2) -
        2 * g * x1 - 2 * f * y1);

    # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
    # where centre is (h = -g, k = -f) and
    # radius r as r^2 = h^2 + k^2 - c
    h = -g;
    k = -f;
    sqr_of_r = h * h + k * k - c;

    # r is the radius
    r = round(sqrt(sqr_of_r), 5);

    return ((h,k),r)

def sharedSegmentPolygon(tri, poly):
    for t in combinations(tri, 2):
        if set(t) in poly:
            return True
    return False

def sharedSegment(tri_a, tri_b):
    for a in combinations(tri_a, 2):
        for b in combinations(tri_b, 2):
            if set(a) == set(b):
                return {frozenset(a)}
    return set()

canvas_width = 800
canvas_height = 600

points=[]
triangles=[]
center_radius=[]
num_of_lines = 0
num_of_circles = 0

# style of diagrams: 0 = hidden, 1 = light, 2 = dark
delaunay=2
voronoi=1
colors={0: "", 1: "#ccc", 2: "#333"}

# whether or not to show vertices
vertexVisible=True

x_coords = []
y_coords = []

def paint(event):
    global points, num_of_lines, num_of_circles, triangles, x_coords, y_coords


    x, y = event.x, event.y

    # don't allow points to be added that are close to each other
    for point in points:
        if dist((x, y), point) < 16:
            return

    # if point shares a coordinate with any other point, add .00001 to avoid colinear points
    while x in x_coords:
        x += .00001
    x_coords.append(x)
    while y in y_coords:
        y += .00001
    y_coords.append(y)


    # keep track of points
    points.append((x, y))
    # index of last point added
    last_point = len(points)-1


    # find out what triangle's circumcircles contain added point
    contains=[]
    for i in range(len(triangles)):
        # compare distance from circumcenter to added point, to circumcircle's radius
        if dist(center_radius[i][0], points[last_point]) < center_radius[i][1]:
            contains.append(i)


    # if more than one triangle's circumcircle contains added point, keep track of segment that needs to be removed
    shared_segments=set()
    for combo in combinations(contains, 2):

        # pair of triangles that contain point
        tri_a = triangles[combo[0]]
        tri_b = triangles[combo[1]]

        # if two triangles share a segment, the segment needs to be removed to form the polygon that the added points needs to form new triangles
        shared_segments = shared_segments.union(sharedSegment(tri_a, tri_b))


    # reverse sort the list of triangles whose circumcircle contains added point, in order to remove from "triangles" list
    contains.sort(reverse=True)
    # vertices of new triangles
    vertices_of_new_triangles=set()
    # keep track of all of the segments of the triangles to be removed
    all_segments=set()


    for i in contains:
        # remove triangle
        tri = triangles.pop(i)
        # remove center_radius associated with removed triangle
        center_radius.pop(i)
        # get vertices of removed triangle, which added point needs, to form new triangles
        vertices_of_new_triangles = vertices_of_new_triangles.union(tri)
        # get segments of removed triangle
        for tri_segment in combinations(tri, 2):
            all_segments = all_segments.union({frozenset(tri_segment)})


    # create a polygon, which the added point needs to share a segment with, in order to add a triangle
    polygon_segments = all_segments.difference(shared_segments)


    # create triangles with added point and all the vertices of triangles that were removed
    for tri in combinations(list(vertices_of_new_triangles | {last_point}), 3):
        # if triangle vertices contain added point, use triangle
        if last_point in tri:
            # if triangle shares a segment of the polygon of triangles whose circumcircles contained the added point, add triangle
            if sharedSegmentPolygon(tri, polygon_segments):
                triangles.append(tri)
                # keep track of center_radius of triangle's circumcircle
                center_radius.append(findCircle(triangles[len(triangles)-1]))

    w.delete("voronoi")
    # draw voronoi diagram
    for combo in combinations(range(len(triangles)), 2):

        # pair of triangles
        tri_a = triangles[combo[0]]
        tri_b = triangles[combo[1]]

        # if two triangles share a segment, draw a line connecting their circumcircle's center
        if sharedSegment(tri_a, tri_b) != set():
            w.create_line(center_radius[combo[0]][0], center_radius[combo[1]][0], fill=colors[voronoi], width=1, tag="voronoi")

    w.delete("delaunay")
    # draw triangles
    for i in range(len(triangles)):
        # don't draw any triangles that are formed using super triangle vertices
        if any(x in triangles[i] for x in [0,1,2]):
            continue

        w.create_polygon(points[triangles[i][0]], points[triangles[i][1]], points[triangles[i][2]], fill="", width=1, outline=colors[delaunay], tag="delaunay")
        # points of voronoi diagram
        # w.create_circle(center_radius[i][0][0], center_radius[i][0][1], 4, fill="green", tag="voronoi")


    # draw vertex
    if vertexVisible:
        w.create_circle(x, y, 4, fill="#0080ff", outline="#000", tag="vertex")
    else:
        w.create_circle(x, y, 4, fill="", outline="", tag="vertex")

    reorderItems()

def reorderItems():
    # move items to front if diagram option is 2
    if delaunay == 2:
        w.tag_raise("delaunay")
    if voronoi == 2:
        w.tag_raise("voronoi")
    # always move vertices to front
    w.tag_raise("vertex")

def changeDiagramStyle(event):
    global delaunay, voronoi

    if event.char == 'd':
        delaunay = (delaunay + 1) % 3
        # ternary operator example
        # w.itemconfig("delaunay", outline="#000" if delaunay == 2 else "#ccc" if delaunay == 1 else "")
        w.itemconfig("delaunay", outline=colors[delaunay])
    elif event.char == 'v':
        voronoi = (voronoi + 1) % 3
        w.itemconfig("voronoi", fill=colors[voronoi])

    reorderItems()

def toggleVertices(event):
    global vertexVisible

    vertexVisible = not vertexVisible
    if vertexVisible:
        w.itemconfig("vertex", fill="#0080ff", outline="#000")
    else:
        w.itemconfig("vertex", fill="", outline="")

def clearPoints(event):
    global points, triangles, center_radius

    # keep first three points of super triangle
    points = points[:3]

    # reset triangles to only have super triangle
    triangles=[(0,1,2)]
    center_radius=[findCircle((0,1,2))]

    # clear canvas
    w.delete("all")

master = Tk()
master.title("")

# create points for super triangle
points.append((400,7800))
points.append((-5600,-4200))
points.append((6400,-4200))

# add super triangle
triangles.append((0,1,2))
# keep track of center_radius of triangle's circumcircle
center_radius.append(findCircle((0,1,2)))

w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack(expand=YES, fill=BOTH)
w.bind("<ButtonRelease-1>", paint)
# press 'd' to change style of delaunay diagram
w.bind_all("<d>", changeDiagramStyle)
# press 'v' to change style of voronoi diagram
w.bind_all("<v>", changeDiagramStyle)
# press 'p' to toggle vertex visibility
w.bind_all("<p>", toggleVertices)
# press 'c' to clear all points
w.bind_all("<c>", clearPoints)

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

# add some sample points
sample = [(400, 323), (402, 461), (588, 444), (594, 296), (533, 237), (398, 197), (312, 350), (174, 133), (146, 368), (215, 270), (192, 489), (203, 430), (303, 15), (316, 135), (449, 18), (618, 139), (521, 131), (712, 188), (618, 531),  (713, 501)]
for p in sample:
    paint(Point(p[0], p[1]))


mainloop()