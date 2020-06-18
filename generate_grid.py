import turtle
import tkinter
import random
import find_path_turtle


# creates the gui and the lines

root = tkinter.Tk()
root.resizable(False, False)
size_x = 400
size_y = 400
gap = 20
root.geometry(str(size_x+10)+'x'+str(size_y+10))
canvas = tkinter.Canvas(root, width=size_x, height=size_y)
t = turtle.TurtleScreen(canvas)
t.setworldcoordinates(0, size_y, size_x, 0)
for x in range(50):
    canvas.create_line(x*gap, 0, x*gap, size_y)
for y in range(50):
    canvas.create_line(0, y*gap, size_x, y*gap)


# randomly generates a grid like maze

grid = []
for x in range(size_x//gap):
    row = []
    for y in range(size_y//gap):
        r = random.random()
        if r <= .8:
            row.append(0)
        else:
            row.append(3)
    grid.append(row)


# loops through grid to see where to create a black square

for y in range(len(grid)):
    # print(grid[y])
    for x in range(len(grid[y])):
        if grid[y][x] == 3:
            canvas.create_rectangle((x*gap, y*gap, (x*gap)+gap, (y*gap)+gap), fill='black')


# randomly gets the indexes from a list so that copies of the same coordinates are not possible

indexes = [x for x in range(size_x//gap)]
rs = indexes[random.randrange(0, len(indexes))]
indexes.remove(rs)
cs = indexes[random.randrange(0, len(indexes))]
indexes.remove(cs)
rt = indexes[random.randrange(0, len(indexes))]
indexes.remove(rt)
ct = indexes[random.randrange(0, len(indexes))]
indexes.remove(ct)

# randomly generates where the turtle will start and where it will go to.

grid[cs][rs] = 1
grid[ct][rt] = 2
canvas.create_rectangle((rs*gap, cs*gap, (rs*gap)+gap, (cs*gap)+gap), fill='green')
canvas.create_rectangle((rt*gap, ct*gap, (rt*gap)+gap, (ct*gap)+gap), fill='red')

# sets the turtles position.

tt = turtle.RawTurtle(t)
tt.penup()
tt.setpos((rs*gap+gap//2, cs*gap+gap//2))
tt.pendown()

# some settings that have to be set that lets the gui be seen correctly. Some are required some are not.

canvas.grid(column=0, row=0)
canvas.bind()
canvas.pack()
tt._delay(20)


def get_grid_and_solve():
    # puts the location of the black squares, start, and stop positions in a dictionary
    d = find_path_turtle.establish_knowns(grid)
    # list to contain all the possible paths to target location.
    paths = []
    # function that recursively finds all the possible paths to location.
    find_path_turtle.find_path(d['s'], [], set(), d, grid, paths)
    # sorts the paths list based on length
    paths.sort(key=len)
    # loops through all the paths
    for x in paths:
        # resets the turtles location.
        tt.penup()
        tt.setpos((rs*gap+gap//2, cs*gap+gap//2))
        tt.pendown()

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
    t.mainloop()



if __name__ == "__main__":
    # error handler just in case there isn't a possible solution
    try:
        get_grid_and_solve()
    except:
        print("Could not be solved")