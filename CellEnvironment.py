from deer.base_classes import Environment
from model.grid import Grid
from model.controller import Controller
from model.cell import CancerCell, HealthyCell


class CellEnvironment(Environment):
    def __init__(self):
        self.grid = None
        self.controller = None

    def reset(self, mode):
        if mode == -1 or True:
            self.grid = Grid(100, 100, glucose=True, oxygen=True, cells=True, border=False, sources=150)
            self.controller = Controller(self.grid, glucose=True, draw_step=0, hcells=1000, oxygen=True, draw_mode='cells',
                                         cancercells=True, oar=(0, 0))
            for i in range(500):
                self.controller.go()

    def act(self, action):
        self.grid.irradiate(action, 50,50, 5, 3)
        self.controller.go()

    def inTerminalState(self):
        return CancerCell.cell_count < 10

    def nActions(self):
        return [.0, 10.0]

    def end(self):
        del self.grid
        del self.controller

    def inputDimensions(self):
        return [(1,), (1,)]

    # TODO
    def observationType(self, subject):
        return 0

    def observe(self):
        return [CancerCell.cell_count, HealthyCell.cell_count]

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)
