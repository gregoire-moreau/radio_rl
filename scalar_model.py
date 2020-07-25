import math
import matplotlib.pyplot as plt
from model.cell import CancerCell, HealthyCell, OARCell
import random

alpha_tumor = 0.3
beta_tumor = 0.03
alpha_norm_tissue = 0.15
beta_norm_tissue = 0.03


class ScalarModel:

    def __init__(self):
        HealthyCell.cell_count = 0
        CancerCell.cell_count = 0
        self.time = 0
        self.ticks = [self.time]
        self.cells = [CancerCell(0)] + [HealthyCell(0) for _ in range(5)]
        self.ccell_counts = [CancerCell.cell_count]
        self.hcell_counts = [HealthyCell.cell_count]
        self.glucose = 100
        self.oxygen = 1000

    def cycle_cells(self):
        to_add = []
        count = HealthyCell.cell_count + CancerCell.cell_count
        for cell in random.sample(self.cells, count):
            res = cell.cycle(self.glucose, count / 5 , self.oxygen)
            if len(res) > 2:  # If there are more than two arguments, a new cell must be created
                if res[2] == 0:  # Mitosis of a healthy cell
                    to_add.append(HealthyCell(0))
                elif res[2] == 1:
                    to_add.append(CancerCell(0))
            self.glucose -= res[0]  # The local variables are updated according to the cell's consumption
            self.oxygen -= res[1]
        self.cells = [cell for cell in self.cells if cell.alive] + to_add

    def fill_sources(self):
        self.glucose += 130
        self.oxygen += 4500

    def go(self, ticks=1):
        for _ in range(ticks):
            self.time += 1
            self.fill_sources()
            self.cycle_cells()
            #graph
            self.ticks.append(self.time)
            self.ccell_counts.append(CancerCell.cell_count)
            self.hcell_counts.append(HealthyCell.cell_count)

    def irradiate(self, dose):
        for cell in self.cells:
            cell.radiate(dose)
        self.cells = [cell for cell in self.cells if cell.alive]

    def draw(self, title):
        plt.plot(self.ticks, self.ccell_counts, 'r', label='Cancer cells')
        plt.plot(self.ticks, self.hcell_counts, 'b', label='Healthy cells')
        #plt.yscale('log')
        plt.xlabel('Hours')
        plt.ylabel("Count")
        plt.legend()
        plt.title(title)
        plt.savefig(''.join(title.lower().split()))

random.seed(1234)
avg = 0
model = ScalarModel()
k = 0
while CancerCell.cell_count > 0 and k < 200:
    k += 1
    model.go()

while CancerCell.cell_count > 0:
    model.irradiate(5)
    model.go(24)


model.draw('Baseline treatment')
