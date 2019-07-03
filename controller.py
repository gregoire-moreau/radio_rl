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
            self.cell_density_plot = None
            self.glucose_plot = None
            self.oxygen_plot = None
            self.cell_plot = None
            self.fig = None
            self.plot_init()

    def plot_init(self):
        matplotlib.use("TkAgg")
        plt.ion()
        self.fig, axs = plt.subplots(2,2, constrained_layout=True)
        self.fig.suptitle('Cell proliferation at t = '+str(self.tick))
        self.glucose_plot = axs[0][0]
        self.glucose_plot.set_title('Glucose density')
        self.cell_plot = axs[1][0]
        self.cell_plot.set_title('Types of cells')
        self.oxygen_plot = axs[0][1]
        self.oxygen_plot.set_title('Oxygen density')
        self.cell_density_plot = axs[1][1]
        self.cell_density_plot.set_title('Cell density')
        self.cell_plot.imshow(
          [[patch_type(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
        self.glucose_plot.imshow(self.grid.glucose)
        self.oxygen_plot.imshow(self.grid.oxygen)
        self.cell_density_plot.imshow(
            [[len(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])

    def go(self):
        self.grid.fill_source(100, 4500)
        self.grid.cycle_cells()
        self.tick += 1
        if self.tick >= 750 and self.tick% 24 ==0:
            grid.irradiate(4,50,50,30,3)
        self.grid.diffuse_glucose(0.9)
        self.grid.diffuse_oxygen(0.9)
        print("Tick :", self.tick, "HealthyCells : ", HealthyCell.cell_count, "CancerCells : ", CancerCell.cell_count,
              "Blood Vessels : ", len(self.grid.sources))
        if self.draw_step > 0 and self.tick % self.draw_step == 0:
            plt.pause(0.02)
            if self.draw_mode == 'cells':
                self.fig.suptitle('Cell proliferation at t = '+str(self.tick))
                self.cell_plot.imshow(
                    [[patch_type(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
                self.glucose_plot.imshow(self.grid.glucose)
                self.oxygen_plot.imshow(self.grid.oxygen)
                self.cell_density_plot.imshow(
                    [[len(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])


def patch_type(patch):
    if len(patch) == 0:
        return 0
    else:
        return patch[0].cell_type()


if __name__ == '__main__':
    random.seed(9)
    grid = Grid(100, 100, glucose = True, oxygen = True, cells = True, border = False, sources=250)
    controller = Controller(grid, glucose = True,  draw_step = 24, hcells = 1000, oxygen=True, draw_mode= 'cells', cancercells=True)
    for i in range(10000):
        controller.go()
    #plt.ioff()
    #plt.show()