from cell import HealthyCell, CancerCell
import numpy as np
import random


class Grid:
    def __init__(self, xsize, ysize, glucose=False, cells=False, oxygen=False, border=False, sources=[]):
        self.xsize = xsize
        self.ysize = ysize
        if glucose:
            self.glucose = [[100 for i in range(self.ysize)] for j in range(xsize)]
        if cells:
            self.cells = [[[] for i in range(self.ysize)] for j in range(self.xsize)]
        if oxygen:
            print("OXYGEN")
        if border:
            self.sources = [(0, i) for i in range(ysize)]+ [(i, 0) for i in range(xsize)]\
                           + [(xsize-1, i) for i in range(ysize)]+ [(i, ysize-1) for i in range(xsize)]
        else:
            self.sources = sources

    def fill_source(self, glucose=0, oxygen=0):
        if glucose != 0:
            for (x, y) in self.sources:
                self.glucose[x][y] = glucose
        if oxygen != 0:
            for (x, y) in self.sources:
                self.oxygen[x][y] = oxygen

    def diffuse_glucose(self, drate):
        new_array = [[0 for i in range(self.ysize)] for j in range(self.xsize)]
        for x in range(self.xsize):
            for y in range(self.ysize):
                new_array[x][y] = (1.0-drate)*self.glucose[x][y] + 0.125*drate*self.neighbors_glucose(x, y)
        self.glucose = new_array

    def neighbors_glucose(self, x, y):
        sum = 0.0
        for (i, j) in [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                sum += self.glucose[i][j]
        return sum

    def cycle_cells(self):
        tot_count = 0
        for i in range(self.xsize):
            for j in range(self.ysize):
                count = len(self.cells[i][j])
                glucose = self.glucose[i][j]
                neigh = self.neighbors(i, j)
                for cell in self.cells[i][j]:
                    gluc = cell.cycle(self.glucose[i][j] / count, count + sum(v for x,y,v in neigh))
                    if isinstance(gluc, tuple):
                        glucose -= gluc[0]
                        if gluc[1] == 0:
                            downhill = rand_min(neigh)
                            self.cells[neigh[downhill][0]][neigh[downhill][1]].append(HealthyCell(0))
                        else:
                            downhill = random.randint(0, len(neigh)-1)
                            self.cells[neigh[downhill][0]][neigh[downhill][1]].append(CancerCell(0))
                        neigh[downhill][2] += 1
                    else:
                        glucose -= gluc
                    if not cell.alive:
                        count -= 1
                self.glucose[i][j] = glucose
                self.cells[i][j] = [cell for cell in self.cells[i][j] if cell.alive]
                tot_count += count
        return tot_count

    def neighbors(self, x, y):
        sum = []
        for (i, j) in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                sum.append([i, j, len(self.cells[i][j])])
        return sum


def rand_min(neigh):
    v = 1000000
    ind = []
    for i in range(len(neigh)):
        if neigh[i][2] < v:
            ind = [i]
        elif neigh[i][2] == v:
            ind.append(i)
    return random.choice(ind)
