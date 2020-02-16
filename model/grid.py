from model.cell import HealthyCell, CancerCell, OARCell, critical_oxygen_level, critical_glucose_level
import numpy as np
import random
import math
import scipy.special


occlusion_number = 6
sqrt_2_pi = math.sqrt(2*math.pi)


class Grid:
    def __init__(self, xsize, ysize, glucose=False, cells=False, oxygen=False, border=False, sources=0, oar=None):
        self.xsize = xsize
        self.ysize = ysize
        if glucose:
            self.glucose = [[100 for i in range(self.ysize)] for j in range(xsize)]
        if cells:
            self.cells = [[[] for i in range(self.ysize)] for j in range(self.xsize)]
        if oxygen:
            self.oxygen = [[10000 for i in range(self.ysize)] for j in range(xsize)]
        if border:
            self.sources = [(0, i) for i in range(ysize)]+ [(i, 0) for i in range(xsize)]\
                           + [(xsize-1, i) for i in range(ysize)]+ [(i, ysize-1) for i in range(xsize)]
            self.num_sources = 2*xsize+2*ysize-4
        else:
            self.num_sources = sources
            self.sources = random_sources(xsize, ysize, sources)
        self.neigh_counts = None
        self.oar = oar

    def count_neigbors(self):
        self.neigh_counts = [[len(self.cells[j][i])+sum(v for x,y, v in self.neighbors(j, i)) for i in range(self.ysize)] for j in range(self.xsize)]

    # Sources of nutrients are refilled
    def fill_source(self, glucose=0, oxygen=0):
        # self.sources = [(x, y) for (x, y) in self.sources if len(self.cells[x][y]) < occlusion_number]
        if glucose != 0:
            for (x, y) in self.sources:
                self.glucose[x][y] += glucose
        if oxygen != 0:
            for (x, y) in self.sources:
                self.oxygen[x][y] += oxygen

    # drate = diffusion rate : percentage of glucose that one patch loses to its neighbors
    def diffuse_glucose(self, drate):
        self.glucose = (1-drate)*np.array(self.glucose)+(0.125*drate)*self.neighbors_glucose()

    def diffuse_oxygen(self, drate):
        self.oxygen = (1 - drate) * np.array(self.oxygen) + (0.125*drate) * self.neighbors_oxygen()

    def neighbors_glucose(self):
        down = np.roll(self.glucose, 1, axis= 0)
        up = np.roll(self.glucose, -1, axis=0)
        right = np.roll(self.glucose, 1, axis=(0, 1))
        left = np.roll(self.glucose, -1, axis=(0, 1))
        down_right = np.roll(down, 1, axis=(0, 1))
        down_left = np.roll(down, -1, axis=(0, 1))
        up_right = np.roll(up, 1, axis=(0, 1))
        up_left = np.roll(up, -1, axis=(0, 1))
        for i in range(self.ysize):  # Down
            down[0][i] = 0
            down_left[0][i] = 0
            down_right[0][i] = 0
        for i in range(self.ysize):  # Up
            up[self.xsize-1][i] = 0
            up_left[self.xsize - 1][i] = 0
            up_right[self.xsize - 1][i] = 0
        for i in range(self.xsize):  # Right
            right[i][0] = 0
            down_right[i][0] = 0
            up_right[i][0] = 0
        for i in range(self.xsize):  # Left
            left[i][self.ysize-1] = 0
            down_left[i][self.ysize-1] = 0
            up_left[i][self.ysize-1] = 0
        return down+up+right+left+down_left+down_right+up_left+up_right

    def neighbors_oxygen(self):
        down = np.roll(self.oxygen, 1, axis= 0)
        up = np.roll(self.oxygen, -1, axis=0)
        right = np.roll(self.oxygen, 1, axis=(0, 1))
        left = np.roll(self.oxygen, -1, axis=(0, 1))
        down_right = np.roll(down, 1, axis=(0, 1))
        down_left = np.roll(down, -1, axis=(0, 1))
        up_right = np.roll(up, 1, axis=(0, 1))
        up_left = np.roll(up, -1, axis=(0, 1))
        for i in range(self.ysize):  # Down
            down[0][i] = 0
            down_left[0][i] = 0
            down_right[0][i] = 0
        for i in range(self.ysize):  # Up
            up[self.xsize-1][i] = 0
            up_left[self.xsize - 1][i] = 0
            up_right[self.xsize - 1][i] = 0
        for i in range(self.xsize):  # Right
            right[i][0] = 0
            down_right[i][0] = 0
            up_right[i][0] = 0
        for i in range(self.xsize):  # Left
            left[i][self.ysize-1] = 0
            down_left[i][self.ysize-1] = 0
            up_left[i][self.ysize-1] = 0
        return down+up+right+left+down_left+down_right+up_left+up_right

    def cycle_cells(self):
        tot_count = 0
        for i in range(self.xsize):
            for j in range(self.ysize): #For every tile
                count = len(self.cells[i][j])
                glucose = self.glucose[i][j] #We keep local glucose and oxygen variables that are updated after every cell
                oxygen = self.oxygen[i][j]
                for cell in self.cells[i][j]:
                    res = cell.cycle(self.glucose[i][j] / count,  self.neigh_counts[i][j], self.oxygen[i][j] / count,)
                    if len(res) > 2: #If there are more than two arguments, a new cell must be created
                        if res[2] == 0: # Mitosis of a healthy cell
                            downhill = self.rand_min(i, j)
                            self.cells[downhill[0]][downhill[1]].append(HealthyCell(0))
                            self.add_neigh_count(downhill[0], downhill[1], 1)  # We add 1 to every neigbouring tile's neigbours counter
                        elif res[2] == 1: #Mitosis of a cancer cell
                            downhill = self.rand_neigh(i, j)
                            self.cells[downhill[0]][downhill[1]].append(CancerCell(0, downhill[0], downhill[1]))
                            self.add_neigh_count(downhill[0], downhill[1], 1) #We add 1 to every neigbouring tile's neigbours counter
                        elif res[2] == 2: #Wake up surrounding oar cells
                            self.wake_surrounding_oar(i, j)
                        elif res[2] == 3:
                            downhill = self.find_hole(i, j)
                            if downhill:
                                self.cells[downhill[0]][downhill[1]].append(OARCell(0, 5))
                                self.add_neigh_count(downhill[0], downhill[1], 1)  # We add 1 to every neigbouring tile's neigbours counter
                            else:
                                cell.stage = 4
                                cell.age = 0
                    glucose -= res[0] #The local variables are updated according to the cell's consumption
                    oxygen -= res[1]
                    if not cell.alive:
                        count -= 1
                        self.add_neigh_count(i, j, -1) #We remove 1 from every neigbouring tile's neigbours counter
                self.glucose[i][j] = glucose #The global glucose and oxygen variables are updated after we cycled every cell on the tile
                self.oxygen[i][j] = oxygen
                #TODO what do I do with dead cells? Should I consider that they take up space? Should they only disappear after some time?
                self.cells[i][j] = [cell for cell in self.cells[i][j] if cell.alive] #Removes all the dead cells from the tile so that the objects are deleted
                self.cells[i][j].sort() #sort so that the cancer cells are first
                # Angiogenesis
                #TODO favor angiogenesis
                '''
                if (oxygen < len(self.cells[i][j])*critical_oxygen_level
                    or glucose < critical_glucose_level*len(self.cells[i][j]))\
                        and (i, j) not in self.sources: # if one nutrient is low and they are still cells on the tile
                    if random.random() < (self.num_sources-len(self.sources))/(self.num_sources*2):
                        self.sources.append((i,j))
                '''
                tot_count += count
        return tot_count

    def wake_surrounding_oar(self, x, y):
        for (i, j) in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1),
                       (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize and i+j <= self.oar[0] + self.oar[1]):
                for oarcell in [c for c in self.cells[i][j] if isinstance(c, OARCell)]:
                    oarcell.stage = 0
                    oarcell.age = 0

    def find_hole(self, x, y):
        l = []
        for (i, j) in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1),
                       (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize and i + j <= self.oar[0] + self.oar[1] ):
                if len([c for c in self.cells[i][j] if isinstance(c, OARCell)]) == 0:
                    l.append((i, j, len(self.cells[i][j])))
        if len(l) == 0:
            return None
        else:
            minimum = 1000
            ind = -1
            for i in range(len(l)):
                if l[i][2] < minimum:
                    minimum = l[i][2]
                    ind = i
            return l[ind]


    def neighbors(self, x, y):
        sum = []
        for (i, j) in [(x, y), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                sum.append([i, j, len(self.cells[i][j])])
        return sum

    def irradiate(self, dose, x, y, rad = -1):
        radius = self.tumor_radius()*1.1 if rad == -1 else rad
        if radius == 0:
            return
        multiplicator = dose/conv(radius, 0)
        for i in range(self.xsize):
            for j in range(self.ysize):
                dist = math.sqrt((x-i)**2 + (y-j)**2)
                if dist <= 2*radius:
                    for cell in self.cells[i][j]:
                        cell.radiate(conv(radius, dist)*multiplicator)
                if any((isinstance(cell, OARCell) and not cell.alive) for cell in self.cells[i][j]):
                    self.wake_surrounding_oar(i,j)
                self.cells[i][j] = [cell for cell in self.cells[i][j] if cell.alive]
        self.count_neigbors()
        return radius

    def tumor_radius(self):
        if CancerCell.cell_count > 0:
            max_dist = -1
            for i in range(self.xsize):
                for j in range(self.ysize):
                    if len(self.cells[i][j]) > 0 and self.cells[i][j][0].__class__ == CancerCell:
                        v = self.dist(i, j, self.xsize//2, self.ysize//2)
                        if v > max_dist:
                            max_dist = v
            return max_dist
        else:
            return 0

    def dist(self, x,y, x_center, y_center):
        return math.sqrt((x-x_center)**2 + (y-y_center)**2)

    # Returns the index of one of the neighboring patches with the lowest density of cells
    def rand_min(self, x, y):
        v = 1000000
        ind = []
        for (i, j) in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                if len(self.cells[i][j]) < v:
                    v = len(self.cells[i][j])
                    ind = [(i, j)]
                elif len(self.cells[i][j]) == v:
                    ind.append((i, j))
        return random.choice(ind)

    def rand_neigh(self, x, y):
        ind = []
        for (i, j) in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                    ind.append((i, j))
        return random.choice(ind)

    def add_neigh_count(self, x, y, v):
        for (i, j) in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                self.neigh_counts[i][j] += v


# std_dev = 0.4 cm = 1.6 cases
denom = math.sqrt(2)*2.4


def conv(rad, x):
    return scipy.special.erf((rad-x)/denom)-scipy.special.erf((-rad-x)/denom)


# Creates a list of random positions in the grid where the sources of nutrients (blood vessels) will be
def random_sources(xsize, ysize, number):
    src = []
    for _ in range(number):
        x = random.randint(0, xsize-1)
        y = random.randint(0, ysize-1)
        if (x, y) not in src:
            src.append((x,y))
    return src
