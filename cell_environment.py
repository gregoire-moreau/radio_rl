from deer.base_classes import Environment
from model.grid import Grid
from model.controller import Controller
import numpy as np
from model.cell import CancerCell, HealthyCell, OARCell
import copy
import cv2


def patch_type(patch):
    if len(patch) == 0:
        return 0
    else:
        return patch[0].cell_type()*len(patch)


class CellEnvironment(Environment):
    def __init__(self):
        HealthyCell.cell_count = 0
        CancerCell.cell_count = 0
        OARCell.cell_count = 0
        self.grid = None
        self.controller = None
        self.grid = Grid(50,  50, glucose=True, oxygen=True, cells=True, border=False, sources=150)
        self.controller = Controller(self.grid, glucose=True, draw_step=0, hcells=1000, oxygen=True,
                                     cancercells=True, oar=(0, 0))
        for i in range(500):
            self.controller.go()
        self.current_controller = copy.deepcopy(self.controller)
        self.num = 0
        self.h_cell_reset = HealthyCell.cell_count
        self.c_cell_reset = CancerCell.cell_count
        self.oar_cell_reset = OARCell.cell_count
        self.draw = False

    def reset(self, mode):
        if mode == -1 or True:
            if ((self.num+1) % 25) == 0 and False:
                self.__init__()
            if self.draw and hasattr(self.current_controller, 'fig'):
                # self.current_controller.fig.ioff()
                self.current_controller.fig.show()

            self.num += 1
            self.current_controller = copy.deepcopy(self.controller)

            if self.draw and self.num % 5 == 0:
                self.current_controller.plot_init()

            HealthyCell.cell_count = self.h_cell_reset
            CancerCell.cell_count = self.c_cell_reset
            OARCell.cell_count = self.oar_cell_reset

    def act(self, action):
        pre_hcell = HealthyCell.cell_count
        pre_ccell = CancerCell.cell_count
        pre_oarcell = OARCell.cell_count
        self.current_controller.grid.irradiate(action, 25, 25)
        post_hcell = HealthyCell.cell_count
        post_ccell = CancerCell.cell_count
        post_oarcell = OARCell.cell_count
        print("Radiation dose :", action, "Gy", (pre_ccell - post_ccell),
              CancerCell.cell_count)
        for _ in range(24):
            self.current_controller.go()

        if self.draw and self.num % 5 == 0 and (self.inTerminalState() or self.current_controller.tick % 12 == 0):
            self.current_controller.update_plots()

        if self.inTerminalState():
            if CancerCell.cell_count > HealthyCell.cell_count:
                return -100000
            else: return 100000
        return (pre_ccell-post_ccell)-5*(pre_hcell-post_hcell)-OARCell.worth*(pre_oarcell-post_oarcell)

    def inTerminalState(self):
        if CancerCell.cell_count <= 0 :
            print("No more cancer, healthy cells lost = ", self.h_cell_reset - HealthyCell.cell_count)
            return True
        elif HealthyCell.cell_count < 10:
            print("Cancer wins, healthy cells lost = ",  self.h_cell_reset - HealthyCell.cell_count)
            return True
        else:
            return False

    def nActions(self):
        return [[0, 10]]

    def end(self):
        del self.grid
        del self.controller

    def inputDimensions(self):
        return [(1, 1), (1, 1), (1, 20,  20)]

    def observe(self):
        cell_types = np.array([[patch_type(self.current_controller.grid.cells[i][j])
                                                                for j in range(self.current_controller.grid.ysize)]
                                                                for i in range(self.current_controller.grid.xsize)], dtype=np.float32)
        return [CancerCell.cell_count, HealthyCell.cell_count, cv2.resize(cell_types,
                                                                dsize=(20,20), interpolation=cv2.INTER_CUBIC)]

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)



