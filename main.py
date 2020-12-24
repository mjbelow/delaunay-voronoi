from tkinter import *

canvas_width = 800
canvas_height = 600

points=[]

def paint(event):
    x1, y1 = (event.x - 4), (event.y - 4)
    x2, y2 = (event.x + 4), (event.y + 4)
    w.create_oval(x1, y1, x2, y2, fill="#0080ff", tag="vertex")

    num_of_lines = 0
    w.delete("segment")
    points.append((event.x, event.y))
    for a in range(len(points)):
        point = points[a]
        for b in range(len(points)):
            # don't draw a line to an already visited vertex
            if b > a:
                w.create_line(point,points[b], tag="segment")
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