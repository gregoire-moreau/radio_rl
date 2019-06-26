import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from grid import Grid
from cell import HealthyCell
import random


class Controller:

    def __init__(self, grid, glucose = False, hcells = 0, oxygen = False, draw_step = 1, draw_mode = 'glucose'):
        self.grid = grid
        self.tick = 0
        self.glucose = glucose
        self.oxygen = oxygen
        self.draw_step = draw_step
        self.draw_mode = draw_mode
        for i in range(hcells):
            new_cell = HealthyCell(random.randint(0,4))
            self.grid.cells[random.randint(0, grid.xsize-1)][random.randint(0, grid.ysize-1)].append(new_cell)
        if draw_step > 0:
            matplotlib.use("TkAgg")
            plt.ion()
            if draw_mode == 'cells':
                plt.imshow([[len(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
            elif draw_mode == 'glucose':
                plt.imshow(self.grid.glucose)

    def go(self):
        self.grid.fill_source(100)
        cell_count = self.grid.cycle_cells()
        self.tick += 1
        self.grid.diffuse_glucose(0.5)
        print("Tick :", self.tick, "Cells : ", cell_count)
        if self.draw_step > 0 and self.tick % self.draw_step == 0:
            plt.pause(0.02)
            if self.draw_mode == 'cells':
                plt.imshow([[len(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
            elif self.draw_mode == 'glucose':
                plt.imshow(self.grid.glucose)


if __name__ == '__main__':
    grid = Grid(50, 50, glucose = True, border = False, sources=[(25,25)], cells = True)
    controller = Controller(grid, glucose = True, draw_step = 100, hcells = 500, draw_mode= 'cells')
    for i in range(10000):
        controller.go()
    #plt.ioff()
    #plt.show()