import matplotlib.pyplot as plt
import matplotlib
from model.grid import Grid
from model.cell import HealthyCell, CancerCell, OARCell
import random


class Controller:

    def __init__(self, grid, glucose = False, hcells = 0, oxygen = False, draw_step = 1, draw_mode = 'glucose',
                 cancercells=False, oar=(0,0)):
        self.grid = grid
        self.tick = 0
        self.glucose = glucose
        self.oxygen = oxygen
        self.draw_step = draw_step
        self.draw_mode = draw_mode
        for i in range(2*oar[0]):
            for j in range(2*oar[1]):
                if i+j <= oar[0]+oar[1]:
                    self.grid.cells[i][j].append(OARCell(0))
        for i in range(hcells):
            new_cell = HealthyCell(random.randint(0, 4))
            x = random.randint(0, grid.xsize - 1)
            y = random.randint(0, grid.ysize - 1)
            while x+y <= oar[0]+oar[1]:
                x = random.randint(0, grid.xsize - 1)
                y = random.randint(0, grid.ysize - 1)
            self.grid.cells[x][y].append(new_cell)
        if cancercells:
            new_cell = CancerCell(random.randint(0, 3))
            self.grid.cells[grid.xsize//2][grid.ysize//2].append(new_cell)
        self.hcells = hcells

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
                [[patch_type(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
            self.cell_density_plot.imshow(
                [[len(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])
        self.glucose_plot.imshow(self.grid.glucose)
        self.oxygen_plot.imshow(self.grid.oxygen)

    def go(self):
        if self.hcells > 0:
            self.grid.fill_source(200, 4500)
            self.grid.cycle_cells()
        self.tick += 1
        self.grid.diffuse_glucose(0.2)
        self.grid.diffuse_oxygen(0.2)
        if self.draw_step > 0 and self.tick % self.draw_step == 0:
            plt.pause(0.02)
            if self.draw_mode == 'cells':
                self.fig.suptitle('Cell proliferation at t = '+str(self.tick))
                self.glucose_plot.imshow(self.grid.glucose)
                self.oxygen_plot.imshow(self.grid.oxygen)
                if self.hcells > 0:
                    self.cell_plot.imshow(
                        [[patch_type(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in
                         range(self.grid.xsize)])
                    self.cell_density_plot.imshow(
                        [[len(self.grid.cells[i][j]) for j in range(self.grid.ysize)] for i in range(self.grid.xsize)])


def patch_type(patch):
    if len(patch) == 0:
        return 0
    else:
        return patch[0].cell_type()


if __name__ == '__main__':
    random.seed(9)
    grid = Grid(100,100, glucose = True, oxygen = True, cells = True, border = False, sources=150)
    controller = Controller(grid, glucose = True,  draw_step = 12, hcells = 1000, oxygen=True, draw_mode= 'cells',
                            cancercells=True, oar = (5,5))
    for i in range(3000):
        controller.go()
        print("Tick :", i, "HealthyCells : ", HealthyCell.cell_count, "CancerCells : ", CancerCell.cell_count,
              "Blood Vessels : ", len(grid.sources), "OAR cells", OARCell.cell_count)
    plt.ioff()
    plt.show()
