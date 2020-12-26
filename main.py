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

def sharedSegment(tri_a, tri_b):
    for a in set(combinations(tri_a, 2)):
        for b in set(combinations(tri_b, 2)):
            if a == b:
                return a
    return {}

canvas_width = 800
canvas_height = 600

points=[]
triangles=[]
num_of_lines = 0
num_of_circles = 0

def paint(event):
    global points, num_of_lines, num_of_circles

    # keep track of points
    points.append((event.x, event.y))
    
    # index of last point added
    last_point = len(points)-1
    
    # find out what triangle's circumcircles contain added point
    contains=[]
    
    for tri in triangles:
        hkr=findCircle(points[tri[0], points[tri[1]], points[tri[2]])
        
        # compare distance from circumcenter to added point, to circumcircle's radius
        if dist((h[0], k[1]), points[last_point]) < hkr[2]:
            contains.append(tri)
            
    # if more than one triangle's circumcircle contains added point, keep track of segment that needs to be removed
    shared_segments=[]
        
    # get all the vertices that added point needs to form new triangles with
    vertices_of_new_triangles=set()
        
    for tri in combinations(contains, 2):
        shared_segment=sharedSegment(tri[0], tri[1])
        if shared_segment != {}:
            # if two triangles share a segment, they need to be removed, and then the point needs to connect to all vertices of these triangles
            vertices_of_new_triangles = vertices_of_new_triangles | (set(tri[0]) | set(tri[1]))
            shared_segments.append(shared_segment)


    # create triangles with added point
    for tri in contains:
    
        
        
    # remove triangles, which contained the point, that had a segment that was shared
    triangles[:] = filterfalse( , triangles)

    # draw vertex
    x1, y1 = (event.x - 4), (event.y - 4)
    x2, y2 = (event.x + 4), (event.y + 4)
    w.create_oval(x1, y1, x2, y2, fill="#0080ff", tag="vertex")


    # draw segments
    w.delete("segment_super")
    for segment in list(combinations(list(range(len(points))), 2)):

        # keep track of segments connecting to super triangle
        if any(n in segment for n in [0, 1, 2]):
            tag="segment_super"
        else:
            tag="segment"
        
        # only draw segments using the last added point
        if last_point in segment:
            w.create_line(points[segment[0]], points[segment[1]], tag=tag)
            num_of_lines=num_of_lines+1

    # draw circumcircles
    w.delete("circumcircle")
    for circle in list(combinations(list(range(len(points))), 3)):

        if last_point in circle:
            # get center and radius of circle given 3 points, each containing last point added
            hkr=findCircle(points[circle[0]], points[circle[1]], points[circle[2]])

            # draw circle
            w.create_circle(hkr[0], hkr[1], hkr[2], tag="circumcircle")

            num_of_circles=num_of_circles+1

    print("lines",num_of_lines)
    print("circles",num_of_circles)



master = Tk()
master.title("")

# create points for super triangle
points.append((400,-300))
points.append((-200,900))
points.append((1200,900))

# add super triangle
triangles.append((0,1,2))

w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack(expand=YES, fill=BOTH)
w.bind("<ButtonRelease-1>", paint)



mainloop()