from deer.base_classes import Environment
from model.grid import Grid
from model.controller import Controller
import numpy as np
from model.cell import CancerCell, HealthyCell, OARCell
import copy
import math
#import cv2
import random


def patch_type(patch):
    if len(patch) == 0:
        return 0
    else:
        return sum([c.cell_type() for c in patch])


class CellEnvironment(Environment):
    def __init__(self, obs_type, resize, reward, action_type, special_reward):
        """Constructor of the environment

        Parameters:
        obs_type : Type of observations provided to the agent (segmentation or densities)
        resize : True if the observations should be resized to 25 * 25 arrays
        reward : Type of reward function used ('dose' to minimize the total dose, 'killed' to maximize damage to cancer
                 cells while miniizing damage to healthy tissue and 'oar' to minimize damage to the Organ At Risk
        action_type : 'DQN' means that we have a discrete action domain and 'AC' means that it is continuous
        special_reward : True if the agent should receive a special reward at the end of the episode.
        """
        self.controller = Controller(1000, 50, 50, 100)
        self.controller.go(350)
        self.init_hcell_count = HealthyCell.cell_count
        self.obs_type = obs_type
        self.resize = resize
        self.reward = reward
        self.action_type = action_type
        self.special_reward = special_reward
        self.dose_map = None

    def get_tick(self):
        return self.controller.tick

    def init_dose_map(self):
        self.dose_map = np.zeros((50, 50), dtype=float)
        self.dataset = [[], [], []]
        self.dose_maps = []
        self.tumor_images = []


    def add_radiation(self, dose, radius, center_x, center_y):
        if dose == 0:
            return
        multiplicator = get_multiplicator(dose, radius)
        for x in range(50):
            for y in range(50):
                dist = math.sqrt((center_x - x)**2 + (center_y - y)**2)
                self.dose_map[x, y] += scale(radius, dist, multiplicator)

    def reset(self, mode):
        self.controller = Controller(1000, 50, 50, 100)
        self.controller.go(350)
        self.init_hcell_count =HealthyCell.cell_count
        if mode == -1:
            self.verbose = False
        else :
            self.verbose = True
        self.total_dose = 0
        self.num_doses = 0
        self.radiation_h_killed = 0
        if self.dose_map is not None:
            self.dose_maps.append((self.controller.tick - 350, np.copy(self.dose_map)))
            self.tumor_images.append((self.controller.tick - 350,
                                      self.controller.observeDensity()))
        return self.observe()


    def act(self, action):
        dose = action / 2 if self.action_type == 'DQN' else action[0] * 4 + 1
        rest = 24 if self.action_type == 'DQN' else int(round(action[1] * 60 + 12))
        if self.dose_map is not None:
            self.controller.grid.compute_center()
            x = self.controller.grid.center_x
            y = self.controller.grid.center_y
            tumor_radius = self.controller.grid.tumor_radius(self.controller.grid.center_x, self.controller.grid.center_y)
        pre_hcell = HealthyCell.cell_count
        pre_ccell = CancerCell.cell_count
        self.total_dose += dose
        self.num_doses += 1 if dose > 0 else 0
        self.controller.irradiate(dose)
        self.radiation_h_killed += (pre_hcell - HealthyCell.cell_count)
        if self.dose_map is not None:
            self.add_radiation(dose, tumor_radius, x, y)
            self.dataset[0].append(self.controller.tick - 350)
            self.dataset[1].append((pre_ccell, CancerCell.cell_count))
            self.dataset[2].append(dose)
            self.dose_maps.append((self.controller.tick - 350, np.copy(self.dose_map)))
            self.tumor_images.append((self.controller.tick - 350, self.controller.observeDensity()))
        p_hcell = HealthyCell.cell_count
        p_ccell = CancerCell.cell_count
        self.controller.go(rest)
        post_hcell = HealthyCell.cell_count
        post_ccell = CancerCell.cell_count
        reward = self.adjust_reward(dose, pre_ccell - post_ccell, pre_hcell-min(post_hcell, p_hcell))
        if self.verbose:
                print("Radiation dose :", dose, "Gy ", "remaining :", post_ccell,  "time =", rest, "reward=", reward)
        return reward

    def adjust_reward(self, dose, ccell_killed, hcells_lost):
        if self.special_reward and self.inTerminalState() or False:
            if self.end_type == "L" or self.end_type == "T":
                return -1
            else:
                if self.reward == 'dose':
                    return - dose / 400 + 0.5 - (self.init_hcell_count - HealthyCell.cell_count) / 3000
                else:
                    return 0.5 - (self.init_hcell_count - HealthyCell.cell_count) / 3000#(cppCellModel.HCellCount() / self.init_hcell_count) - 0.5 - (2 * hcells_lost/2500)
        else:
            if self.reward == 'dose' or self.reward == 'oar':
                return - dose / 400 + (ccell_killed - 5 * hcells_lost)/100000
            elif self.reward == 'killed':
                return (ccell_killed - 5 * hcells_lost)/100000


    def inTerminalState(self):
        if CancerCell.cell_count <= 0 :
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
        if self.action_type == 'DQN':
            return 9
        elif self.action_type == 'DDPG':
            return [[0, 1], [0, 1], [0, 1]] if self.tumor_radius else [[0, 1], [0, 1]]

    def end(self):
        del self.controller

    def inputDimensions(self):
        if self.resize:
            tab = [(1, 25, 25)]
        else:
            tab = [(1, 50, 50)]
        return tab

    def observe(self):
        if self.obs_type == 'densities':
            cells = (np.array(self.controller.observeDensity(), dtype=np.float32)) / 100.0
        else:
            cells = (np.array(self.controller.observeSegmentation(), dtype=np.float32) + 1.0) / 2.0 #  Obs from 0 to 1
        if self.resize:
            cells = cv2.resize(cells, dsize=(25,25), interpolation=cv2.INTER_CUBIC)
        return [cells]

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)

def transform(head):
    to_ret = np.zeros(shape=(head.shape[0], head.shape[1], 3), dtype=np.int)
    for i in range(head.shape[0]):
        for j in range(head.shape[1]):
            if head[i][j] == 1:
                to_ret[i][j][1] = 120
            elif head[i][j] == -1:
                to_ret[i][j][0] = 120
    return to_ret


def transform_densities(obs):
    to_ret = np.zeros(shape=(obs.shape[0], obs.shape[1], 3), dtype=np.int)
    for i in range(obs.shape[0]):
        for j in range(obs.shape[1]):
            if obs[i][j] < 0:
                to_ret[i][j][0] = 60 + min(- obs[i][j] * 4, 195)
            elif obs[i][j] > 0:
                to_ret[i][j][1] = 60 + min(obs[i][j] * 8, 195)
    return to_ret

def conv(rad, x):
    denom = 3.8 # //sqrt(2) * 2.7
    return math.erf((rad - x)/denom) - math.erf((-rad - x) / denom)


def get_multiplicator(dose, radius):
    return dose / conv(14, 0)


def scale(radius, x, multiplicator):
    return multiplicator * conv(14, x * 10 / radius)