import matplotlib.pyplot as plt
import matplotlib
from model.grid import Grid
from model.cell import HealthyCell, CancerCell, OARCell
import random
from threading import Thread
import numpy as np


class Controller:

    def __init__(self, grid, glucose = False, hcells = 0, oxygen = False, draw_step = 0,
                 cancercells=False, oar=(0,0)):
        self.grid = grid
        self.tick = 0
        self.glucose = glucose
        self.oxygen = oxygen
        self.draw_step = draw_step
        for i in range(2*oar[0]):
            for j in range(2*oar[1]):
                if i+j <= oar[0]+oar[1]:
                    self.grid.cells[i][j].append(OARCell(4, 5))
        for i in range(hcells):
            new_cell = HealthyCell(random.randint(0, 4))
            x = random.randint(0, grid.xsize - 1)
            y = random.randint(0, grid.ysize - 1)
            while x+y <= oar[0]+oar[1]:
                x = random.randint(0, grid.xsize - 1)
                y = random.randint(0, grid.ysize - 1)
            self.grid.cells[x][y].append(new_cell)
        if cancercells:
            new_cell = CancerCell(random.randint(0, 3), grid.xsize//2, grid.ysize//2)
            CancerCell.center = (grid.xsize//2, grid.ysize//2)
            self.grid.cells[grid.xsize//2][grid.ysize//2].append(new_cell)
        self.hcells = hcells

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
    def go(self):
        if self.hcells > 0:
            self.grid.fill_source(100, 4500)
            self.grid.cycle_cells()
        self.tick += 1
        self.grid.diffuse_glucose(0.2)
        self.grid.diffuse_oxygen(0.2)
        if self.draw_step > 0 and self.tick % self.draw_step == 0:
            self.update_plots()

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


def patch_type_color(patch):
    if len(patch) == 0:
        return 0, 0, 0
    else:
        return patch[0].cell_color()


class SimThread(Thread):
    def __init__(self, row_1, row_2, cell_rows, glucose_rows, oxy_rows, neigh_counts):
        Thread.__init__(self)
        self.row_1 = row_1
        self.row_2 = row_2
        self.xsize = row_2-row_1
        self.ysize = len(cell_rows[0])
        self.cell_rows = cell_rows
        self.glucose_rows = glucose_rows
        self.oxy_rows = oxy_rows
        self.neigh_counts = neigh_counts
        self.mode = None
        self.new_cells = []
        self.removed = []

    def run(self):
        if self.mode == 'cycle':
            self.new_cells = []
            self.removed = []
            self.cycle()
        elif self.mode == 'diffuse':
            pass



    def rand_min(self, x, y):
        v = 1000000
        ind = []
        for (i, j) in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                if len(self.cell_rows[i][j]) < v:
                    v = len(self.cell_rows[i][j])
                    ind = [(i, j)]
                elif len(self.cell_rows[i][j]) == v:
                    ind.append((i, j))
        return random.choice(ind)

    def rand_neigh(self, x, y):
        ind = []
        for (i, j) in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y),
                       (x + 1, y + 1)]:
            if (i >= 0 and i < self.xsize and j >= 0 and j < self.ysize):
                    ind.append((i, j))
        return random.choice(ind)

    def cycle(self):
        for i in range(len(self.cell_rows)):
            for j in range(len(self.cell_rows[i])):  # For every tile
                count = len(self.cell_rows[i][j])
                glucose = self.glucose_rows[i][j]  # We keep local glucose and oxygen variables that are updated after every cell
                oxygen = self.oxy_rows[i][j]
                for cell in self.cell_rows[i][j]:
                    res = cell.cycle(glucose, self.neigh_counts[i][j], oxygen )
                    if len(res) > 2:  # If there are more than two arguments, a new cell must be created
                        if res[2] == 0:  # Mitosis of a healthy cell
                            downhill = self.rand_min(i, j)
                            #self.cells[downhill[0]][downhill[1]].append(HealthyCell(0))
                            self.new_cells.append((HealthyCell(0), downhill[0]+ self.row_1, downhill[1]))
                        else:  # Mitosis of a cancer cell
                            downhill = self.rand_neigh(i, j)
                            self.new_cells.append((CancerCell(0, downhill[0]+self.row_1, downhill[1]), downhill[0] + self.row_1, downhill[1]))
                            #self.cells[downhill[0]][downhill[1]].append()
                            #self.add_neigh_count(downhill[0], downhill[1],1)  # We add 1 to every neigbouring tile's neigbours counter
                    glucose -= res[0]  # The local variables are updated according to the cell's consumption
                    oxygen -= res[1]
                    if not cell.alive:
                        count -= 1
                        #self.add_neigh_count(i, j, -1)  # We remove 1 from every neigbouring tile's neigbours counter
                        self.removed.append((i+self.row_1, j))
                self.glucose_rows[i][j] = glucose  # The global glucose and oxygen variables are updated after we cycled every cell on the tile
                self.oxy_rows[i][j] = oxygen
                # TODO what do I do with dead cells? Should I consider that they take up space? Should they only disappear after some time?
                self.cell_rows[i][j] = [cell for cell in self.cell_rows[i][j] if
                                    cell.alive]  # Removes all the dead cells from the tile so that the objects are deleted
                self.cell_rows[i][j].sort()  # sort so that the cancer cells are first


class MultiThreadController:
    def __init__(self,  grid:Grid, hcells=0, thread_number=1):
        self.grid = grid
        self.tick = 0
        for i in range(hcells):
            new_cell = HealthyCell(random.randint(0, 4))
            x = random.randint(0, grid.xsize - 1)
            y = random.randint(0, grid.ysize - 1)
            self.grid.cells[x][y].append(new_cell)
        new_cell = CancerCell(random.randint(0, 3), grid.xsize // 2, grid.ysize // 2)
        CancerCell.center = (grid.xsize // 2, grid.ysize // 2)
        self.grid.cells[grid.xsize // 2][grid.ysize // 2].append(new_cell)
        self.grid.count_neigbors()
        #create threads
        self.rows = [int(round(i)) for i in np.linspace(0, grid.xsize, thread_number+1)]
        self.threads = []
        self.thread_number = thread_number


    def go(self, n_hours=1):
        for _ in range(n_hours):
            threads = []
            for i in range(self.thread_number):
                up = self.rows[i]
                down = self.rows[i + 1]
                thread = SimThread(up, down, self.grid.cells[up:down], self.grid.glucose[up:down], self.grid.oxygen[up:down],
                                   self.grid.neigh_counts[up: down])
                threads.append(thread)
            self.grid.fill_source(100, 4500)
            for thread in threads:
                thread.mode = 'cycle'
                thread.start()
            cells_to_add = []
            cells_removed = []
            for thread in threads:
                thread.join()
                cells_to_add += thread.new_cells
                cells_removed += thread.removed
            for cell in cells_to_add:
                self.grid.cells[cell[1]][cell[2]].append(cell[0])
                self.grid.add_neigh_count(cell[1], cell[2], 1)
            for to_rem in cells_removed:
                self.grid.add_neigh_count(to_rem[0], to_rem[1], -1)
            #change cells
            self.grid.diffuse_glucose(0.2)
            self.grid.diffuse_oxygen(0.2)
            '''
            for thread in self.threads:
                thread.mode = 'diffuse'
                thread.start()
            for thread in self.threads:
                thread.join()
            '''
            self.tick += 1
            #print(self.tick)



if __name__ == '__main__':
    random.seed(4775)
    grid = Grid(50,50, glucose=True, oxygen=True, cells= True, border = False, sources=50, oar=(15,15))
    controller = Controller(grid, glucose = True,  draw_step=0, hcells = 500, oxygen=True,
                            cancercells=True, oar = (15, 15))
    #controller = MultiThreadController(grid, 1000, 1)
    #controller.go(1000)
    k = 1
    for i in range(2000):
        controller.go()

        #print("Tick :", i, "HealthyCells : ", HealthyCell.cell_count, "CancerCells : ", CancerCell.cell_count,
              "Blood Vessels : ", len(grid.sources), "OAR cells", OARCell.cell_count)
        
        if i == 2000:
            break


        if i > 400 and i % 24 == 0:
            grid.irradiate(2,25,25)



        # DQN
        '''
        if i == 408:
            grid.irradiate(4.5,25,25)
        if i == 432 or i == 456 or i == 480:
            grid.irradiate(5,25,25)
        if i > 500 and i % 24 == 0:
            grid.irradiate(2,25,25)
        '''


        # DDPG
        '''
        if i > 400 and i % 24 == 0:
            if k % 5 == 0:
                grid.irradiate(3.5,25,25)
            else :
                grid.irradiate(1.5,25,25)
            k+=1
        '''

    '''
    print(HealthyCell.cell_count)

    plt.ioff()
    plt.show()
    '''