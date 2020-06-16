import matplotlib.pyplot as plt
import matplotlib
from model.grid import Grid
from model.cell import HealthyCell, CancerCell, OARCell
import random
import numpy as np


class Controller:

    def __init__(self, hcells, xsize, ysize, sources, draw_step = 0):
        self.grid = Grid(xsize, ysize, sources)
        self.tick = 0
        self.hcells = hcells
        self.draw_step = draw_step
        self.xsize = xsize
        self.ysize = ysize
        HealthyCell.cell_count = 0
        CancerCell.cell_count = 0
        prob = hcells / (xsize * ysize)
        for i in range(xsize):
            for j in range(ysize):
                if random.random() < prob:
                    new_cell = HealthyCell(random.randint(0, 4))
                    self.grid.cells[i, j].append(new_cell)
        new_cell = CancerCell(random.randint(0, 3))
        self.grid.cells[self.xsize//2, self.ysize//2].append(new_cell)

        self.grid.count_neigbors()

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
        if self.hcells > 0:
            self.cell_plot.imshow(
                [[patch_type_color(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
            self.cell_density_plot.imshow(
                [[len(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
        self.glucose_plot.imshow(self.grid.glucose)
        self.oxygen_plot.imshow(self.grid.oxygen)

    # Simulates one hour on the grid : Nutrient diffusion and replenishment, cell cycle
    def go(self, steps=1):
        for _ in range(steps):
            self.grid.fill_source(130, 4500)
            self.grid.cycle_cells()
            self.grid.diffuse_glucose(0.2)
            self.grid.diffuse_oxygen(0.2)
            self.tick += 1
            if self.draw_step > 0 and self.tick % self.draw_step == 0:
                self.update_plots()
            if self.tick % 24 == 0:
                self.grid.compute_center()

    def irradiate(self, dose):
        """Irradiate the tumour"""
        self.grid.irradiate(dose)

    def update_plots(self):
        self.fig.suptitle('Cell proliferation at t = ' + str(self.tick))
        self.glucose_plot.imshow(self.grid.glucose)
        self.oxygen_plot.imshow(self.grid.oxygen)
        if self.hcells > 0:
            self.cell_plot.imshow(
                [[patch_type_color(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in
                range(self.grid.xsize)])
            self.cell_density_plot.imshow(
                [[len(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
        plt.pause(0.02)

    def observeSegmentation(self):
        """Produce observation of type segmentation"""
        seg = np.vectorize(lambda x:x.pixel_type())
        return seg(self.grid.cells)

    def observeDensity(self):
        """Produce observation of type densities"""
        dens = np.vectorize(lambda x: x.pixel_density())
        return dens(self.grid.cells)



def patch_type_color(patch):
    if len(patch) == 0:
        return 0, 0, 0
    else:
        return patch[0].cell_color()

if __name__ == '__main__':
    random.seed(4775)
    count = 0
    for i in range(100):
        print(i)
        controller = Controller(1000, 50, 50, 100 )
        controller.go(350)
        for i in range(35):
            controller.irradiate(2)
            controller.go(24)
        if CancerCell.cell_count == 0:
            count += 1
    print(count)
    '''
    print(CancerCell.cell_count)
    controller.go()
    print(CancerCell.avg_repair)
    for _ in range(35):
        ticks.append(controller.tick)
        cancer_cells.append(CancerCell.cell_count)
        controller.irradiate(2)
        ticks.append(controller.tick)
        cancer_cells.append(CancerCell.cell_count)
        controller.go(24)
    plt.plot(ticks, cancer_cells)
    plt.show()
    '''