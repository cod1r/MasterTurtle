import random

def grid_make():
    """
    A test function to generate a random grid.
    """
    grid = []
    size_x = 800
    size_y = 800
    gap = 15
    for x in range(size_x//gap):
        row = []
        for y in range(size_y//gap):
            r = random.random()
            if r <= .7:
                row.append(0)
            else:
                row.append(3)
        grid.append(row)
    indexes = [x for x in range(size_x//gap)]
    rs = indexes[random.randrange(0, len(indexes))]
    indexes.remove(rs)
    cs = indexes[random.randrange(0, len(indexes))]
    indexes.remove(cs)
    rt = indexes[random.randrange(0, len(indexes))]
    indexes.remove(rt)
    ct = indexes[random.randrange(0, len(indexes))]
    indexes.remove(ct)
    grid[rs][cs] = 1
    grid[rt][ct] = 2
    # for x in grid:
    #     print(x)
    return grid

def establish_knowns(grid):
    """
    Function to return dictionary that has the walls, start, and stop locations.
    """
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

# NOTE: old class
# class that contains a variable to help the find_path function know which "node" to prioritize.
# class Node:
#     def __init__(self, g, loc):
#         self.g = g
#         self.loc = loc


# returns the euclidean distance between two points
def calc(pA, pB):
    """returns the euclidean distance between two points"""
    return (pA[0]-pB[0])**2+(pA[1]-pB[1])**2

# NOTE: OLD CODE/OLD IMPLEMENTATION
# needs optimizations badly. VERY BADLY
# def find_path(loc, path, been_to, d, grid, paths):
#     """
#     Recursively returns the paths to target location borrowing a simple heuristic from popular path finding algorithms which is the euclidean distance. 
#     This function isn't the best or efficient but it works and displays a fun gui.
#     """
#     if len(paths) == 0 and loc == d['t'] and tuple(path) not in paths:
#         path.append(loc)
#         paths.add(tuple(path))
#         return True
#     elif len(paths) > 0 and len(min(paths, key=len)) > len(path) and loc == d['t'] and tuple(path) not in paths:
#         # print(len(path), len(paths))
#         path.append(loc)
#         paths.add(tuple(path))
#         return True
#     elif len(paths) == 0 or len(path) < len(min(paths, key=len)) and tuple(path) not in paths:
#         been_to.add(loc)
#         path.append(loc)
#         options = []
#         if loc[0] + 1 < len(grid) and 0 <= loc[1] < len(grid[loc[0]]) and (loc[0]+1, loc[1]) not in been_to and (loc[0]+1, loc[1]) not in d['w']:
#             n = Node(calc((loc[0]+1, loc[1]), d['t']), (loc[0]+1, loc[1]))
#             options.append(n)
#         if loc[0] - 1 >= 0 and 0 <= loc[1] < len(grid[loc[0]]) and (loc[0] - 1, loc[1]) not in been_to and (loc[0]-1, loc[1]) not in d['w']:
#             n = Node(calc((loc[0]-1, loc[1]), d['t']), (loc[0]-1, loc[1]))
#             options.append(n)
#         if loc[1] + 1 < len(grid[0]) and 0 <= loc[0] < len(grid) and (loc[0], loc[1] + 1) not in been_to and (loc[0], loc[1] + 1) not in d['w']:
#             n = Node(calc((loc[0], loc[1]+1), d['t']), (loc[0], loc[1]+1))
#             options.append(n)
#         if loc[1] - 1 >= 0 and 0 <= loc[0] < len(grid) and (loc[0], loc[1] - 1) not in been_to and (loc[0], loc[1] - 1) not in d['w']:
#             n = Node(calc((loc[0], loc[1]-1), d['t']), (loc[0], loc[1]-1))
#             options.append(n)
#         if len(options) == 0 or (len(paths) > 0 and len(path) > len(min(paths, key=len))) or tuple(path) in paths:
#             return False
#         options.sort(key=lambda x: x.g)
#         for x in options:
#             been_to_copy = been_to.copy()
#             find_path(x.loc, path[:], been_to_copy, d, grid, paths)

# NOTE: NEW CLASS
class vertex:
    def __init__(self, weight, loc):
        self.weight = weight
        self.loc = loc
        self.visited = False


# NOTE: NEW IMPLEMENTATION/ DIKJSTRAS ALGORITHM!!!!!!!!!!!
def Dijkstras(grid, info):
    nodes = [ [ vertex(float('inf'), (r, c)) for c in range(len(grid[r])) ] for r in range(len(grid)) ]
    path = {}
    vertexes = []
    for _ in nodes:
        for v in _:
            path[v.loc] = []
            vertexes.append(v)

    vertexes[(info['s'][0])*len(grid)+(info['s'][1])].weight = 0

    # print("start", vertexes[(info['s'][0])*len(grid)+(info['s'][1])].loc)
    # print("length of list", len(vertexes))
    while True:
        # print(list(map(lambda x: x.loc, path)))
        _min = vertex(float('inf'), None)
        i = 0
        for v in range(len(vertexes)):
            if _min.weight > vertexes[v].weight:
                _min = vertexes[v]
                i = v
        
        
        if (_min.loc == info['t']):
            print("DONE")
            break

        if not (_min.loc[0] + 1 >= len(grid)) and not vertexes[(_min.loc[0] + 1)*len(grid) + (_min.loc[1])].visited and vertexes[(_min.loc[0] + 1)*len(grid) + (_min.loc[1])].loc not in info['w']:

            # print(1, vertexes[(_min.loc[0] + 1)*len(grid) + (_min.loc[1])].loc)
            path[vertexes[(_min.loc[0] + 1)*len(grid) + (_min.loc[1])].loc].append(_min.loc)
            vertexes[(_min.loc[0] + 1)*len(grid) + (_min.loc[1])].weight = min(vertexes[(_min.loc[0] + 1)*len(grid) + (_min.loc[1])].weight, _min.weight + calc(info['s'], (_min.loc[0] + 1, _min.loc[1])))

        if not (_min.loc[0] - 1 < 0) and not vertexes[(_min.loc[0] - 1)*len(grid) + (_min.loc[1])].visited and vertexes[(_min.loc[0] - 1)*len(grid) + (_min.loc[1])].loc not in info['w']:

            # print(2, vertexes[(_min.loc[0] - 1)*len(grid) + (_min.loc[1])].loc)
            path[vertexes[(_min.loc[0] - 1)*len(grid) + (_min.loc[1])].loc].append(_min.loc)
            vertexes[(_min.loc[0] - 1)*len(grid) + (_min.loc[1])].weight = min(vertexes[(_min.loc[0] - 1)*len(grid) + (_min.loc[1])].weight, _min.weight + calc(info['s'], (_min.loc[0] - 1, _min.loc[1])))

        if not (_min.loc[1] + 1 >= len(grid[0])) and not vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] + 1)].visited and vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] + 1)].loc not in info['w']:

            # print(3, vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] + 1)].loc)
            path[vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] + 1)].loc].append(_min.loc)
            vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] + 1)].weight = min(vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] + 1)].weight, _min.weight + calc(info['s'], (_min.loc[0], _min.loc[1] + 1)))
        
        if not (_min.loc[1] - 1 < 0) and not vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] - 1)].visited and vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] - 1)].loc not in info['w']:

            # print(4, vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] - 1)].loc)
            path[vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] - 1)].loc].append(_min.loc)
            vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] - 1)].weight = min(vertexes[(_min.loc[0])*len(grid) + (_min.loc[1] - 1)].weight, _min.weight + calc(info['s'], (_min.loc[0], _min.loc[1] - 1)))

        vertexes[i].weight = float('inf')
        vertexes[i].visited = True

    journey = [info['t']]
    curr = path[info['t']][0]
    while True:
        if curr == info['s']:
            journey.append(curr)
            break
        journey.append(curr)
        curr = path[curr][0]

    return journey[::-1]
        
            
    

if __name__ == "__main__":
    grid = grid_make()
    print(len(grid), len(grid[0]))
    for x in grid:
        print(x)
    d = establish_knowns(grid)
    print("start: ", d['s'], "end: ", d['t'])
    # paths = set()
    # been_to = set()
    # find_path(d['s'], [], been_to, d, grid, paths)
    paths = Dijkstras(grid, d)
    print(paths)