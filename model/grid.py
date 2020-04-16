from model.cell import HealthyCell, CancerCell, OARCell, critical_oxygen_level, critical_glucose_level
import numpy as np
import random
import math
import scipy.special


sqrt_2_pi = math.sqrt(2*math.pi)


class Grid:
    """The grid is the base of the simulation.

    It is made out of 3 superimposed 2D layers : one contains the CellLists foreach pixel,
    one contains the glucose amount on each pixel and one contains the oxygen amount on each pixel.
    """

    def __init__(self, xsize, ysize,  sources, oar=None):
        """Constructor of the Grid.

        Parameters :
        xsize : Number of rows of the grid
        ysize : Number of cclumns of the grid
        sources : Number of nutrient sources on the grid
        oar : Optional description of an OAR zone on the grid
        """
        self.xsize = xsize
        self.ysize = ysize

        self.glucose = np.full((xsize, ysize), 100.0)
        self.oxygen = np.full((xsize, ysize), 10000.0)
        # Helpers are useful because diffusion cannot be done efficiently in place.
        # With a helper array of same shape, we can simply compute the result inside the other and alternate between
        # the arrays.
        self.glucose_helper = np.full((xsize, ysize), 100.0)
        self.oxygen_helper = np.full((xsize, ysize), 10000.0)

        self.cells = np.empty((xsize, ysize), dtype=object)
        for i in range(xsize):
            for j in range(ysize):
                self.cells[i, j] = []

        self.num_sources = sources
        self.sources = random_sources(xsize, ysize, sources)

        # Neigbor counts contain, for each pixel on the grid, the number of cells on neigboring pixels. They are useful
        # as HealthyCells only reproduce in case of low density. As these counts seldom change after a few hundred
        # simulated hours, it is more efficient to store them than simply recompute them for each pixel while cycling.
        self.neigh_counts = np.zeros((xsize, ysize), )

        self.oar = oar

    def count_neigbors(self):
        """Compute the neigbour counts (the number of cells on neighbouring pixels) for each pixel"""
        for i in self.xsize:
            for j in self.ysize:
                self.neigh_counts[i, j] = sum(v for _, _, v in self.neighbors(i, j))

    def fill_source(self, glucose=0, oxygen=0):
        """Sources of nutrients are refilled."""
        if glucose != 0:
            for (i, j) in self.sources:
                self.glucose[i, j] += glucose
        if oxygen != 0:
            for (i, j) in self.sources:
                self.oxygen[i, j] += oxygen

    def diffuse_glucose(self, drate):
        """Diffuse glucose on the grid

        Parameters:
        drate : diffusion rate : percentage of glucose that one patch loses to its neighbors
        """
        self.diffuse_helper(self.glucose, self.glucose_helper, drate)
        self.glucose, self.glucose_helper = self.glucose_helper, self.glucose

    def diffuse_oxygen(self, drate):
        """Diffuse glucose on the grid

        Parameters:
        drate : diffusion rate : percentage of oxygen that one patch loses to its neighbors
        """
        self.diffuse_helper(self.glucose, self.glucose_helper, drate)
        self.oxygen, self.oxygen_helper = self.oxygen_helper, self.oxygen

    def diffuse_helper(self, src, dest, drate):
        base = 1 - drate
        neigh = drate * 0.125
        for i in range(self.xsize):
            for j in range(self.ysize):
                dest[i, j] = base * src[i, j]  # First keep the base amount
            for j in range(1, self.ysize):
                dest[i, j] += neigh * src[i, j - 1]  # Diffusion to the right
            for j in range(self.ysize - 1):
                dest[i, j] += neigh * src[i, j + 1]  # Diffusion to the left
        for i in range(self.xsize - 1):
            for j in range(self.ysize):
                dest[i, j] += neigh * src[i + 1, j]  # Diffusion to the top
            for j in range(self.ysize - 1):
                dest[i, j] += neigh * src[i + 1, j + 1]  # Diffusion to top left
            for j in range(1, self.ysize):
                dest[i, j] += neigh * src[i + 1, j - 1]  # Diffusion to top right
        for i in range(1, self.xsize):
            for j in range(self.ysize):
                dest[i, j] += neigh * src[i - 1, j]  # Diffusion to the bottom
            for j in range(self.ysize - 1):
                dest[i, j] += neigh * src[i - 1, j + 1]  # Diffusion to bottom left
            for j in range(1, self.ysize):
                dest[i, j] += neigh * src[i - 1, j - 1]  # Diffusion to bottom right

    def cycle_cells(self):
        tot_count = 0
        for i in range(self.xsize):
            for j in range(self.ysize):  # For every pixel
                count = len(self.cells[i][j])
                for cell in self.cells[i][j]:
                    res = cell.cycle(self.glucose[i, j],  self.neigh_counts[i, j], self.oxygen[i, j])
                    if len(res) > 2:  # If there are more than two arguments, a new cell must be created
                        if res[2] == 0: # Mitosis of a healthy cell
                            downhill = self.rand_min(i, j)
                            self.cells[downhill[0], downhill[1]].append(HealthyCell(0))
                            self.add_neigh_count(downhill[0], downhill[1], 1)  # We add 1 to every neigbouring tile's neigbours counter
                        elif res[2] == 1:  # Mitosis of a cancer cell
                            downhill = self.rand_neigh(i, j)
                            self.cells[downhill[0]][downhill[1]].append(CancerCell(0, downhill[0], downhill[1]))
                            self.add_neigh_count(downhill[0], downhill[1], 1)  # We add 1 to every neigbouring tile's neigbours counter
                        elif res[2] == 2:  # Wake up surrounding oar cells
                            self.wake_surrounding_oar(i, j)
                        elif res[2] == 3:
                            downhill = self.find_hole(i, j)
                            if downhill:
                                self.cells[downhill[0]][downhill[1]].append(OARCell(0, 5))
                                self.add_neigh_count(downhill[0], downhill[1], 1)  # We add 1 to every neigbouring tile's neigbours counter
                            else:
                                cell.stage = 4
                                cell.age = 0
                    self.glucose[i, j] -= res[0]  # The local variables are updated according to the cell's consumption
                    self.oxygen[i, j] -= res[1]
                    if not cell.alive:
                        count -= 1
                        self.add_neigh_count(i, j, -1) #We remove 1 from every neigbouring tile's neigbours counter
                self.cells[i][j] = [cell for cell in self.cells[i][j] if cell.alive] #Removes all the dead cells from the tile so that the objects are deleted
                self.cells[i][j].sort()  # sort so that the cancer cells are first
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
