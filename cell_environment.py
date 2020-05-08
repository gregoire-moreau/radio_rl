from deer.base_classes import Environment
from model.grid import Grid
from model.controller import Controller, MultiThreadController
import numpy as np
from model.cell import CancerCell, HealthyCell, OARCell
import copy
import cv2
import random


def patch_type(patch):
    if len(patch) == 0:
        return 0
    else:
        return sum([c.cell_type() for c in patch])


class CellEnvironment(Environment):
    def __init__(self, obs_type, resize, reward, action_type, tumor_radius, special_reward, dose_map=False):
        self.obs_type = obs_type
        self.resize = resize
        self.reward = reward
        self.action_type = action_type
        self.tumor_radius = tumor_radius
        self.special_reward = special_reward
        random.seed(42)
        HealthyCell.cell_count = 0
        CancerCell.cell_count = 0
        OARCell.cell_count = 0
        self.grid = Grid(50, 50, sources=100, dose_map=dose_map)
        self.controller = None
        self.init_hcell_count = HealthyCell.cell_count
        self.map = False

    def set_map_patient(self, map):
        self.controller = None

    def reset(self, mode):
        if not self.map:
            HealthyCell.cell_count = 0
            CancerCell.cell_count = 0
            OARCell.cell_count = 0
            self.grid = Grid(50, 50, glucose=True, oxygen=True, cells=True, border=False, sources=50, oar=(15, 15))
            self.controller = Controller(self.grid, glucose=True, draw_step=0, hcells=500, oxygen=True,
                                 cancercells=True, oar=(15, 15))
            for i in range(400):
                self.controller.go()
        self.init_hcell_count = HealthyCell.cell_count
        if mode == -1:
            self.verbose = True
        else:
            self.verbose = True
        return self.observe()

    def act(self, action):
        dose = action / 2 if self.action_type == 'DQN' else action[0]
        rest = 24 if self.action_type == 'DQN' else int(round(action[1]))

        pre_hcell = HealthyCell.cell_count
        pre_ccell = CancerCell.cell_count
        pre_oar_cell = OARCell.cell_count

        self.controller.grid.irradiate(dose, 25, 25)
        for i in range(rest):
            self.controller.go()

        post_hcell = HealthyCell.cell_count
        post_ccell = CancerCell.cell_count
        post_oar_cell = OARCell.cell_count

        if self.verbose:
            if self.reward != 'oar':
                print("Radiation dose :", dose, "Gy ",
                      "remaining :", post_ccell, "time =", rest)
            else:
                print("Radiation dose :", dose, "Gy ",
                      "remaining :", post_ccell, "time =", rest, "radius =",
                      0)

        return self.adjust_reward(dose, post_ccell - pre_ccell, post_hcell - pre_hcell, post_oar_cell - pre_oar_cell)

    def adjust_reward(self, dose, ccell_killed, hcell_lost, oar_lost):
        if self.special_reward and self.inTerminalState():
            if self.end_type == "L" or self.end_type == "T":
                return -1
            else:
                if self.reward == 'oar':
                    return OARCell.cell_count / self.init_oar_count
                elif self.reward == 'dose':
                    return HealthyCell.cell_count / self.init_hcell_count
                else:
                    return 1
        else:
            if self.reward == 'dose' or self.reward == 'oar':
                return - dose / 100
            elif self.reward == 'killed':
                return (ccell_killed - 5 * hcell_lost) / 500

    def inTerminalState(self):
        if CancerCell.cell_count <= 0:
            if self.verbose:
                print("No more cancer")
            self.end_type = 'W'
            return True
        elif HealthyCell.cell_count < 10:
            if self.verbose:
                print("Cancer wins")
            self.end_type = "L"
            return True
        elif self.controller.tick > 1550:
            if self.verbose:
                print("Time out!")
            self.end_type = "T"
            return True
        else:
            return False

    def nActions(self):
        return 9 if self.action_type == 'DQN' else [[1, 4], [12, 72]]

    def inputDimensions(self):
        if self.resize:
            tab = [(1, 25, 25)]
        else:
            tab = [(1, 50, 50)]
        if self.tumor_radius:
            tab.append((1,1))
        return tab

    def end(self):
        del self.grid
        del self.controller

    def observe(self):
        cell_types = np.array([[patch_type(self.controller.grid.cells[i][j])
                                                                for j in range(self.controller.grid.ysize)]
                                                                for i in range(self.controller.grid.xsize)], dtype=np.float32)
        return [cv2.resize(cell_types, dsize=(25,25) if self.resize else (50, 50), interpolation=cv2.INTER_CUBIC)]
        #return [CancerCell.cell_count, HealthyCell.cell_count]

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)


    def show_dose_map(self):
        if self.grid:
            pass
