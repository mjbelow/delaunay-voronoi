from tkinter import *
from itertools import *
from math import *

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def findCircle(p1, p2, p3):

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

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

    return (h,k,r)

    # print("Centre = (", h, ", ", k, ")");
    # print("Radius = ", r);

def sharedSegmentPolygon(tri, poly):
    for t in list(combinations(tri, 2)):
        if set(t) in poly:
            return True
    return False
            
def sharedSegment(tri_a, tri_b):
    for a in set(combinations(tri_a, 2)):
        for b in set(combinations(tri_b, 2)):
            if a == b:
                return frozenset(a)
    return {}

canvas_width = 800
canvas_height = 600

points=[]
triangles=[]
num_of_lines = 0
num_of_circles = 0

x_coords = []
y_coords = []

def paint(event):
    global points, num_of_lines, num_of_circles, triangles, x_coords, y_coords

    x, y = event.x, event.y

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
        hkr=findCircle(points[triangles[i][0]], points[triangles[i][1]], points[triangles[i][2]])

        # compare distance from circumcenter to added point, to circumcircle's radius
        if dist((hkr[0], hkr[1]), points[last_point]) < hkr[2]:
            contains.append(i)

    # if more than one triangle's circumcircle contains added point, keep track of segment that needs to be removed
    shared_segments=set()

    # get all the vertices, which added point needs, to add new triangles
    vertices_of_new_triangles=set()
    # get indices of "triangles" list that need to be removed
    triangles_to_be_removed=set()

    for combo in list(combinations(contains, 2)):

        # pair of triangles that contain point
        tri_a = triangles[combo[0]]
        tri_b = triangles[combo[1]]

        # if two triangles share a segment, they need to be removed, and then the point needs to connect to all vertices of these triangles
        shared_segment=sharedSegment(tri_a, tri_b)
        if shared_segment != {}:
            vertices_of_new_triangles = vertices_of_new_triangles | (set(tri_a) | set(tri_b))
            triangles_to_be_removed = triangles_to_be_removed | set(combo)
            
            print("::::::::::::::::::::::::::::::::::")
            print(shared_segment)
            shared_segments = shared_segments.union({shared_segment})
            print(shared_segments)
            
            print("::::::::::::::::::::::::::::::::::")


    # create a list of the indices of triangles to be removed, and reverse order to delete from "triangles" list
    triangles_to_be_removed = list(triangles_to_be_removed)
    triangles_to_be_removed.sort(reverse=True)
    print(triangles)
    print(triangles_to_be_removed)

    # keep track of all of the segments of the triangles to be removed
    all_segments=set()

    # remove triangles, which contained the point, that had a segment that was shared
    for i in triangles_to_be_removed:
        # get segments of removed triangle
        for tri_segment in list(combinations(triangles.pop(i), 2)):
            all_segments = all_segments.union({frozenset(tri_segment)})
            
    # create a polygon, which the added point needs to share a segment with, in order to add a triangle
    polygon_segments = all_segments.difference(shared_segments)

    print("---------------------------------------------")
    print(all_segments)
    print(shared_segments)
    print(polygon_segments)

    print(triangles)
    

    if len(contains) == 1:
        for tri in list(combinations((set(triangles[contains[0]]) | {last_point}), 3)):
            if last_point in tri:
                triangles.append(tri)
        # remove triangle containing point
        triangles.pop(contains[0])
    else:
        # new_triangles=[]
        # create triangles with added point and all the vertices of triangles that were removed
        for tri in list(combinations(list(vertices_of_new_triangles | {last_point}), 3)):
            # if triangle vertices contain added point, use triangle
            if last_point in tri:
            
                # if sharedSegment((0,1,2), tri) != {}:
                    
                    # triangles.append(tri)
                    # continue
                print(tri)
                print(polygon_segments)
                if sharedSegmentPolygon(tri, polygon_segments):
                    print("#########################################################################################################################################")
                    print(tri)
                    triangles.append(tri)

        # update original triangles with new triangles
        # triangles = triangles + new_triangles

    print(triangles)

    # draw vertex
    x1, y1 = (event.x - 4), (event.y - 4)
    x2, y2 = (event.x + 4), (event.y + 4)
    w.create_oval(x1, y1, x2, y2, fill="#0080ff", tag="vertex")



    w.delete("triangle")
    # draw triangles
    for triangle in triangles:
        # print(triangle)
        if any(x in triangle for x in [0,1,2]):
            continue
        w.create_polygon(points[triangle[0]], points[triangle[1]], points[triangle[2]], fill='', width=1, outline='red', tag="triangle")

    print(points)



master = Tk()
master.title("")

# create points for super triangle
points.append((400,-1500))
points.append((-1200,1900))
points.append((2000,1900))

# add super triangle
triangles.append((0,1,2))

w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack(expand=YES, fill=BOTH)
w.bind("<ButtonRelease-1>", paint)

class myPoint:
  def __init__(self, x, y):
    self.x = x
    self.y = y


paint(myPoint(400, 323))
paint(myPoint(420, 423))
paint(myPoint(600, 323))
paint(myPoint(340, 249))
paint(myPoint(269, 414))
paint(myPoint(120, 78))
paint(myPoint(694, 508))
paint(myPoint(481, 177))
paint(myPoint(330, 93))

# another bad case
# [(400, -300), (-400, 900), (1200, 900), (397, 249), (356, 369), (541, 386), (539, 241), (440, 177)]

# [(400, 0), (0, 623), (800, 623), (400, 323), (420, 423), (600, 323.00001), (340, 249), (269, 414), (472, 383), (464, 213), (213, 238), (330, 138), (501, 305), (411, 264), (444, 123), (234, 129), (209, 341), (259, 343)]

# [(400, -200), (0, 600), (800, 600), (400, 323), (420, 423), (600, 323.00001), (340, 249), (269, 414), (482, 215), (376, 190), (271, 163), (240, 265), (199, 317), (199.00001, 165), (440, 130), (285, 74), (98, 347)]



# paint(myPoint(472, 248))
# paint(myPoint(576, 460))


# paint(myPoint(332, 226))
# paint(myPoint(269, 391))
# paint(myPoint(472, 248))
# paint(myPoint(576, 460))
# paint(myPoint(600, 300))


mainloop()