from cell import HealthyCell, CancerCell, critical_oxygen_level, critical_glucose_level
import numpy as np
import random
import math


occlusion_number = 5


class Grid:
    def __init__(self, xsize, ysize, glucose=False, cells=False, oxygen=False, border=False, sources=0):
        self.xsize = xsize
        self.ysize = ysize
        if glucose:
            self.glucose = [[100 for i in range(self.ysize)] for j in range(xsize)]
        if cells:
            self.cells = [[[] for i in range(self.ysize)] for j in range(self.xsize)]
        if oxygen:
            self.oxygen = [[100000 for i in range(self.ysize)] for j in range(xsize)]
        if border:
            self.sources = [(0, i) for i in range(ysize)]+ [(i, 0) for i in range(xsize)]\
                           + [(xsize-1, i) for i in range(ysize)]+ [(i, ysize-1) for i in range(xsize)]
            self.num_sources = 2*xsize+2*ysize-4
        else:
            self.num_sources = sources
            self.sources = random_sources(xsize, ysize, sources)

    def fill_source(self, glucose=0, oxygen=0):
        self.sources = [(x, y) for (x, y) in self.sources if len(self.cells[x][y]) < occlusion_number]
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

    def diffuse_oxygen(self, drate):
        new_array = [[0 for i in range(self.ysize)] for j in range(self.xsize)]
        for x in range(self.xsize):
            for y in range(self.ysize):
                new_array[x][y] = (1.0-drate)*self.oxygen[x][y] + 0.125*drate*self.neighbors_oxygen(x, y)
        self.oxygen = new_array

    def neighbors_glucose(self, x, y):
        sum = 0.0
        for (i, j) in [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                sum += self.glucose[i][j]
        return sum

    def neighbors_oxygen(self, x, y):
        sum = 0.0
        for (i, j) in [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                sum += self.oxygen[i][j]
        return sum

    def cycle_cells(self):
        tot_count = 0
        for i in range(self.xsize):
            for j in range(self.ysize):
                count = len(self.cells[i][j])
                glucose = self.glucose[i][j]
                oxygen = self.oxygen[i][j]
                neigh = self.neighbors(i, j)
                for cell in self.cells[i][j]:
                    res = cell.cycle(self.glucose[i][j] / count,  count + sum(v for x,y,v in neigh), self.oxygen[i][j] / count,)
                    if len(res) > 2:
                        if res[2] == 0:
                            downhill = rand_min(neigh)
                            self.cells[neigh[downhill][0]][neigh[downhill][1]].append(HealthyCell(0))
                        else:
                            downhill = random.randint(0, len(neigh)-1)
                            self.cells[neigh[downhill][0]][neigh[downhill][1]].append(CancerCell(0))
                        neigh[downhill][2] += 1
                    glucose -= res[0]
                    oxygen -= res[1]
                    if not cell.alive:
                        count -= 1
                self.glucose[i][j] = glucose
                self.oxygen[i][j] = oxygen
                self.cells[i][j] = [cell for cell in self.cells[i][j] if cell.alive]
                if (oxygen < len(self.cells[i][j])*critical_oxygen_level
                    or glucose < critical_glucose_level*len(self.cells[i][j]))\
                        and (i, j) not in self.sources:
                    if random.random() < (self.num_sources-len(self.sources))/self.num_sources:
                        # print("Angiogenesis")
                        self.sources.append((i,j))
                tot_count += count
        return tot_count

    def neighbors(self, x, y):
        sum = []
        for (i, j) in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                sum.append([i, j, len(self.cells[i][j])])
        return sum

    def irradiate(self, dose, x, y, radius, bystander_radius):
        for i in range(self.xsize):
            for j in range(self.ysize):
                dist = math.sqrt((x-i)**2 + (y-j)**2)
                if dist <= radius:
                    for cell in self.cells[i][j]:
                        cell.radiate(dose)
                elif dist < radius + bystander_radius:
                    for cell in self.cells[i][j]:
                        cell.bystander_radiation((1/2) *
                                                 math.sqrt(
                                                     (-dist+radius+bystander_radius) *
                                                     (dist+bystander_radius-radius) *
                                                     (dist - bystander_radius + radius) *
                                                     (dist + bystander_radius + radius)
                                                 ))
                self.cells[i][j] = [cell for cell in self.cells[i][j] if cell.alive]


def rand_min(neigh):
    v = 1000000
    ind = []
    for i in range(len(neigh)):
        if neigh[i][2] < v:
            ind = [i]
            v = neigh[i][2]
        elif neigh[i][2] == v:
            ind.append(i)
    return random.choice(ind)


def random_sources(xsize, ysize, number):
    src = []
    for _ in range(number):
        x = random.randint(0, xsize-1)
        y = random.randint(0, ysize-1)
        if (x, y) not in src:
            src.append((x,y))
    return src
