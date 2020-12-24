from tkinter import *
from itertools import *

canvas_width = 800
canvas_height = 600

points=[]
num_of_lines = 0

def paint(event):
    global points, num_of_lines

    # keep track of points
    points.append((event.x, event.y))

    # draw vertex
    x1, y1 = (event.x - 4), (event.y - 4)
    x2, y2 = (event.x + 4), (event.y + 4)
    w.create_oval(x1, y1, x2, y2, fill="#0080ff", tag="vertex")

    # draw segments
    w.delete("segment")
    for segment in list(combinations(list(range(len(points))), 2)):

        # only draw segments using the last added point
        last_point = len(points)-1
        if last_point in segment:
            w.create_line(points[segment[0]], points[segment[1]], tag="segment")
            num_of_lines=num_of_lines+1

    print(num_of_lines)



master = Tk()
master.title("")
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack(expand=YES, fill=BOTH)
w.bind("<ButtonRelease-1>", paint)



mainloop()