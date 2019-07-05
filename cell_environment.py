from deer.base_classes import Environment
from model.grid import Grid
from model.controller import Controller
from model.cell import CancerCell, HealthyCell, OARCell


class CellEnvironment(Environment):
    def __init__(self):
        self.grid = None
        self.controller = None

    def reset(self, mode):
        if mode == -1 or True:
            self.grid = Grid(100, 100, glucose=True, oxygen=True, cells=True, border=False, sources=150)
            self.controller = Controller(self.grid, glucose=True, draw_step=0, hcells=1000, oxygen=True,
                                         cancercells=True, oar=(0, 0))
            for i in range(500):
                self.controller.go()

    def act(self, action):
        pre_hcell = HealthyCell.cell_count
        pre_ccell = CancerCell.cell_count
        pre_oarcell = OARCell.cell_count
        self.grid.irradiate(action[0], 50,50, action[1], 3)
        post_hcell = HealthyCell.cell_count
        post_ccell = CancerCell.cell_count
        post_oarcell = OARCell.cell_count
        print("Radiation dose :", action[0], "Gy, std dev =", action[1],(pre_ccell-post_ccell), CancerCell.cell_count)
        self.controller.go()
        return (pre_ccell-post_ccell)-(pre_hcell-post_hcell)-OARCell.worth*(pre_oarcell-post_oarcell)

    def inTerminalState(self):
        return CancerCell.cell_count < 10 or HealthyCell.cell_count < 10

    def nActions(self):
        return [[0,10],[0,10]]

    def end(self):
        del self.grid
        del self.controller

    def inputDimensions(self):
        return [(1,), (1,)]

    def observe(self):
        return [CancerCell.cell_count, HealthyCell.cell_count]

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)
