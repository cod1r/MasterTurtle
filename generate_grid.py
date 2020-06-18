import turtle
import tkinter
import random
import find_path_turtle



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


for y in range(len(grid)):
    # print(grid[y])
    for x in range(len(grid[y])):
        if grid[y][x] == 3:
            canvas.create_rectangle((x*gap, y*gap, (x*gap)+gap, (y*gap)+gap), fill='black')

grid[0][0] = 1
grid[len(grid)-1][len(grid[0])-1] = 2
canvas.create_rectangle((0, 0, gap, gap), fill='green')
canvas.create_rectangle((size_x-gap, size_y-gap, size_x, size_y), fill='red')
canvas.grid(column=0, row=0)
canvas.bind()
tt = turtle.RawTurtle(t)
tt.penup()
tt.setpos((gap/2, gap/2))
tt.pendown()
canvas.pack()
tt._delay(20)


def get_grid_and_solve():
    d = find_path_turtle.establish_knowns(grid)
    paths = []
    find_path_turtle.find_path(d['s'], [], set(), d, grid, paths)
    x = min(paths, key=len)
    prev = x[0]
    for p in x:
        if p[1] > prev[1]:
            tt.setheading(0)
        elif p[1] < prev[1]:
            tt.setheading(180)
        elif p[0] > prev[0]:
            tt.setheading(90)
        elif p[0] < prev[0]:
            tt.setheading(270)
        tt.goto(p[1]*gap+gap//2, p[0]*gap+gap//2)
        prev = p
    t.mainloop()



if __name__ == "__main__":
    try:
        get_grid_and_solve()
    except:
        print("Could not be solved")