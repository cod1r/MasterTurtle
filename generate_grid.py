import turtle
import tkinter
import random
import find_path_turtle


# creates the gui and the lines

root = tkinter.Tk()
root.resizable(False, False)
size_x = 1000
size_y = 1000
gap = 15
root.geometry(str(size_x+10)+'x'+str(size_y+10))
canvas = tkinter.Canvas(root, width=size_x, height=size_y)
t = turtle.TurtleScreen(canvas)
t.setworldcoordinates(0, size_y, size_x, 0)
for x in range(500):
    canvas.create_line(x*gap, 0, x*gap, size_y)
for y in range(500):
    canvas.create_line(0, y*gap, size_x, y*gap)


# randomly generates a grid like maze

grid = find_path_turtle.grid_make()
d = find_path_turtle.establish_knowns(grid)

# loops through grid to see where to create a black square

for y in range(len(grid)):
    # print(grid[y])
    for x in range(len(grid[y])):
        if grid[y][x] == 3:
            canvas.create_rectangle((x*gap, y*gap, (x*gap)+gap, (y*gap)+gap), fill='black')

canvas.create_rectangle((d['s'][1]*gap, d['s'][0]*gap, (d['s'][1]*gap)+gap, (d['s'][0]*gap)+gap), fill='green')
canvas.create_rectangle((d['t'][1]*gap, d['t'][0]*gap, (d['t'][1]*gap)+gap, (d['t'][0]*gap)+gap), fill='red')

# sets the turtles position.

tt = turtle.RawTurtle(t)
tt.penup()
tt.setpos((d['s'][1]*gap+gap//2, d['s'][0]*gap+gap//2))
tt.pendown()

# some settings that have to be set that lets the gui be seen correctly. Some are required some are not.

canvas.grid(column=0, row=0)
canvas.bind()
canvas.pack()


def get_grid_and_solve():
    # puts the location of the black squares, start, and stop positions in a dictionary
    d = find_path_turtle.establish_knowns(grid)
    # list to contain all the possible paths to target location.
    # paths = set()
    # function that recursively finds all the possible paths to location.
    # find_path_turtle.find_path(d['s'], [], set(), d, grid, paths)
    # sorts the paths list based on length
    # paths.sort(key=len)
    # loops through all the paths
    # for x in paths:
        # resets the turtles location.
        # tt.penup()
        # tt.setpos((rs*gap+gap//2, cs*gap+gap//2))
        # tt.pendown()
    # x = min(paths, key=len)
    x = find_path_turtle.Dijkstras(grid, d)
    # previous coordinate so that it knows how to turn
    prev = x[0]
    for p in x:
        # conditions that turn the turtle
        if p[1] > prev[1]:
            tt.setheading(0)
        elif p[1] < prev[1]:
            tt.setheading(180)
        elif p[0] > prev[0]:
            tt.setheading(90)
        elif p[0] < prev[0]:
            tt.setheading(270)
        # moves the turtle to location.
        tt.goto(p[1]*gap+gap//2, p[0]*gap+gap//2)
        prev = p
    # calls the gui event loop to show the events
    if tt.pos()[0] == (d['t'][1]*gap)+gap//2 and tt.pos()[1] == (d['t'][0]*gap)+gap//2:
        root.after(2000, lambda: root.destroy())
    t.mainloop()



if __name__ == "__main__":
    # error handler just in case there isn't a possible solution
    try:
        get_grid_and_solve()
    except:
        print("Could not be solved")