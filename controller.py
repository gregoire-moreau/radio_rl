import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from grid import Grid
from cell import HealthyCell, CancerCell
import random


class Controller:

    def __init__(self, grid, glucose = False, hcells = 0, oxygen = False, draw_step = 1, draw_mode = 'glucose',
                 cancercells=False):
        self.grid = grid
        self.tick = 0
        self.glucose = glucose
        self.oxygen = oxygen
        self.draw_step = draw_step
        self.draw_mode = draw_mode
        for i in range(hcells):
            new_cell = HealthyCell(random.randint(0, 4))
            self.grid.cells[random.randint(0, grid.xsize-1)][random.randint(0, grid.ysize-1)].append(new_cell)
        if cancercells:
            new_cell = CancerCell(random.randint(0, 3))
            self.grid.cells[grid.xsize//2][grid.ysize//2].append(new_cell)
        if draw_step > 0:
            matplotlib.use("TkAgg")
            plt.ion()
            self.glucose_plot = plt.subplot(121)
            self.cell_plot = plt.subplot(122)
            if draw_mode == 'cells':
                self.cell_plot.imshow([[patch_type(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
                self.glucose_plot.imshow(self.grid.glucose)

    def go(self):
        self.grid.fill_source(100)
        cell_count = self.grid.cycle_cells()
        self.tick += 1
        if self.tick >= 500 and self.tick% 12 ==0:
            grid.irradiate(3,25,25,15,3)
        self.grid.diffuse_glucose(0.9)
        print("Tick :", self.tick, "HealthyCells : ", HealthyCell.cell_count, "CancerCells : ", CancerCell.cell_count)
        if self.draw_step > 0 and self.tick % self.draw_step == 0:
            plt.pause(0.02)
            if self.draw_mode == 'cells':
                self.cell_plot.imshow(
                    [[patch_type(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
                self.glucose_plot.imshow(self.grid.glucose)


def random_sources(xsize, ysize, number):
    src = []
    for _ in range(number):
        x = random.randint(0, xsize-1)
        y = random.randint(0, ysize-1)
        if (x, y) not in src:
            src.append((x,y))
    return src


def patch_type(patch):
    if len(patch) == 0:
        return 0
    else:
        return patch[0].cell_type()


if __name__ == '__main__':
    random.seed(420)
    grid = Grid(50, 50, glucose = True, border = False, sources=random_sources(50,50, 50), cells = True)
    controller = Controller(grid, glucose = True, draw_step = 100, hcells = 500, draw_mode= 'cells', cancercells=True)
    for i in range(10000):
        controller.go()
    #plt.ioff()
    #plt.show()