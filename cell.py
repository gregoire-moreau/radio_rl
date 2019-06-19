import util
import random
from deer.base_classes import Environment

cell_cycle = {'G1':12, 'S':6, 'G2':4, 'm': 2}

class Cell:
    def __init__(self, patch):
        self.age = 0
        self.stage = 'G1'
        self.alive = True
        self.patch = patch

    def tick(self):
        # Absorb oxygen
        self.age += 1
        if False: #Check sufficient energy
            self.alive = False
        elif self.age == cell_cycle[self.stage]:
            self.age = 0
            if self.stage =='m':
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
        self.patch.addCellDivide(Cell(self.patch))

    def irradiate(self, dose):
        fraction = util.survival_fraction(dose)
        prob = random.random()
        if (prob > fraction):
            self.alive = False

class Patch:
    def __init__(self):
        self.num_cells = 0
        self.cells = []
        self.addList = []

    def addCell(self, cell):
        self.num_cells += 1
        self.cells.append(cell)

    def addCellDivide(self, cell):
        self.addList.append(cell)


    def recount(self):
        self.cells[:] = [cell for cell in self.cells if cell.alive]
        self.num_cells = len(self.cells)

    def tick(self):
        for cell in self.cells:
            cell.tick()
        self.cells += self.addList
        self.addList = []
        self.recount()

    def irradiate(self, dose):
        for cell in self.cells:
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