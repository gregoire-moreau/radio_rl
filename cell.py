import util
import random
from deer.base_classes import Environment

cell_cycle = {'G1':12, 'S':6, 'G2':4, 'm': 2}

class Cell:
    def __init__(self, patch, x, y):
        self.age = 0
        self.stage = 'G1'
        self.alive = True
        self.patch = patch
        self.cancer = False
        self.x = x
        self.y = y

    def tick(self):
        if not self.alive:
            return
        # Absorb oxygen
        self.age += 1
        if False: #Check sufficient energy
            self.alive = False
        elif self.age == cell_cycle[self.stage]:
            self.age = 0
            if self.stage =='m':
                if self.cancer:
                    self.divide()
                self.stage = 'G1'
            else:
                if self.stage == 'G1':
                    self.stage = 'S'
                elif self.stage == 'S':
                    self.stage = 'G2'
                elif self.stage == 'G2':
                    self.stage = 'm'

    def divide(self):
        self.patch.spreadCancer(self.x, self.y)

    def irradiate(self, dose):
        fraction = util.survival_fraction(dose)
        prob = random.random()
        if (prob > fraction):
            self.alive = False

class Patch:
    def __init__(self):
        self.num_healthy = 9999
        self.num_cancer = 1
        self.cells = [[Cell(self, i, j) for i in range(100)] for j in range(100)]
        self.cells[49][49].cancer = True


    def spreadCancer(self, x, y):
        for tup in [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]:
            if (tup[0] >= 0 and tup[0] < 100 and tup[1] >= 0 and tup[1] < 100):
                self.cells[tup[0]][tup[1]].cancer = True


    def recount(self):
        self.num_healthy = 0
        self.num_cancer = 0
        for i in range(100):
            for j in range(100):
                if self.cells[i][j].alive:
                    if self.cells[i][j].cancer:
                        self.num_cancer += 1
                    else:
                        self.num_healthy +=1

    def tick(self):
        for row in self.cells:
            for cell in row:
                cell.tick()
        self.recount()

    def irradiate(self, dose):
        for row in self.cells:
            for cell in row:
                cell.irradiate(dose)
        self.recount()


doses = list(range(10))
class Env(Environment):
    def __init__(self):
        self.patch = Patch()
        self.patch.addCell(Cell())

    def act(self, action):
        self.patch.irradiate(doses[action])

    def end(self):
        del self.patch

    def inTerminalState(self):
        self.patch.num_cells == 0

    def nActions(self):
        return 10

    def inputDimensions(self):
        return []

    def observe(self):
        return self.patch.num_cells

    def reset(self, mode):
        self.patch = Patch()
        self.patch.addCell(Cell())