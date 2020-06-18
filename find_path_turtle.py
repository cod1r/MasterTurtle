import random

def grid_make():
    grid = []
    size_x = 200
    size_y = 200
    gap = 20
    for x in range(size_x//gap):
        row = []
        for y in range(size_y//gap):
            r = random.random()
            if r <= .6:
                row.append(0)
            else:
                row.append(3)
        grid.append(row)
    grid[0][0] = 1
    grid[len(grid)-1][len(grid[0])-1] = 2
    # for x in grid:
    #     print(x)
    return grid

def establish_knowns(grid):
    d = {'w':set()}
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == 1:
                d["s"] = (x, y)
            elif grid[x][y] == 2:
                d["t"] = (x, y)
            elif grid[x][y] == 3:
                d["w"].add((x, y))
    return d


class Node:
    def __init__(self, g, loc):
        self.g = g
        self.loc = loc

def calc(pA, pB):
    return (pA[0]-pB[0])**2+(pA[1]-pB[1])**2

def find_path(loc, path, been_to, d, grid, paths):
    if loc == d['t']:
        path.append(loc)
        paths.append(path)
        return True
    else:
        been_to.add(loc)
        path.append(loc)
        options = []
        if loc[0] + 1 < len(grid) and (loc[0]+1, loc[1]) not in been_to and (loc[0]+1, loc[1]) not in d['w']:
            n = Node(calc((loc[0]+1, loc[1]), d['t']), (loc[0]+1, loc[1]))
            options.append(n)
        if loc[0] - 1 >= 0 and (loc[0] - 1, loc[1]) not in been_to and (loc[0]-1, loc[1]) not in d['w']:
            n = Node(calc((loc[0]-1, loc[1]), d['t']), (loc[0]-1, loc[1]))
            options.append(n)
        if loc[1] + 1 < len(grid[0]) and (loc[0], loc[1] + 1) not in been_to and (loc[0], loc[1] + 1) not in d['w']:
            n = Node(calc((loc[0], loc[1]+1), d['t']), (loc[0], loc[1]+1))
            options.append(n)
        if loc[1] - 1 >= 0 and (loc[0], loc[1] - 1) not in been_to and (loc[0], loc[1] - 1) not in d['w']:
            n = Node(calc((loc[0], loc[1]-1), d['t']), (loc[0], loc[1]-1))
            options.append(n)
        if len(options) == 0:
            return False
        options.sort(key=lambda x: x.g)
        # print(len(options))
        for x in options:
            find_path(x.loc, path[:], been_to, d, grid, paths)
                

# find_path(d['s'], [], set())

# print("DONE")