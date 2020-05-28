import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
import matplotlib.colors as mcol
import cv2
import math
try:
    import cppCellModel
except:
    strErr = "\n\n`cppCellModel` module not found, "
    raise RuntimeError(strErr)

from deer.base_classes import Environment


class CellEnvironment(Environment):
    """Environment that the reinforcement learning agent uses to interact with the simulation."""

    def __init__(self, obs_type, resize, reward, action_type, tumor_radius, special_reward, center):
        """Constructor of the environment

        Parameters:
        obs_type : Type of observations provided to the agent ('head' for segmentation or 'types' for weighted sums)
        resize : True if the observations should be resized to 25 * 25 arrays
        reward : Type of reward function used ('dose' to minimize the total dose, 'killed' to maximize damage to cancer
                 cells while miniizing damage to healthy tissue and 'oar' to minimize damage to the Organ At Risk
        action_type : 'DQN' means that we have a discrete action domain and 'AC' means that it is continuous
        tumor_radius : True if the current radius of the tumor should be included as an observation to the agent
        special_reward : True if the agent should receive a special reward at the end of the episode.
        center : True if the irradiation should be centered on the center of the grid
        """
        if reward == 'oar':
            x1 = random.randint(1, 10)
            x2 = random.randint(11, 20)
            y1 = random.randint(1, 10)
            y2 = random.randint(11, 20)
            print("Start with oar x1=", x1, "x2=", x2, "y1=", y1, "y2=", y2)
            self.controller_capsule = cppCellModel.controller_constructor_oar(50, 50, 100, 350, x1, x2, y1, y2)
            self.init_oar_count = cppCellModel.OARCellCount()
        else:
            self.controller_capsule = cppCellModel.controller_constructor(50, 50, 100, 350)
            self.init_hcell_count = cppCellModel.HCellCount()
        self.obs_type = obs_type
        self.resize = resize
        self.reward = reward
        self.action_type = action_type
        self.tumor_radius = tumor_radius
        self.special_reward = special_reward
        self.center = center
        self.dose_map = None

    def get_tick(self):
        return cppCellModel.controllerTick(self.controller_capsule)

    def init_dose_map(self):
        self.dose_map = np.zeros((50, 50), dtype=float)
        self.dataset = [[], [], []]

    def add_radiation(self, dose, radius, center_x, center_y):
        if dose == 0:
            return
        multiplicator = dose / conv(radius, 0)
        for x in range(50):
            for y in range(50):
                dist = math.sqrt((center_x - x)**2 + (center_y - y)**2)
                self.dose_map[x, y] += conv(radius, dist) * multiplicator

    def show_dose_map(self):
        pos = plt.imshow(self.dose_map, cmap=mcol.LinearSegmentedColormap.from_list("MyCmapName",[[0,0,0.6],"r"]))
        plt.colorbar(pos)
        plt.show()

    def reset(self, mode):
        cppCellModel.delete_controller(self.controller_capsule)
        if self.reward == 'oar':
            x1 = random.randint(1, 10)
            x2 = random.randint(11, 20)
            y1 = random.randint(1, 10)
            y2 = random.randint(11, 20)
            print("Start with oar x1=", x1, "x2=", x2, "y1=", y1, "y2=", y2)
            self.controller_capsule = cppCellModel.controller_constructor_oar(50, 50, 50, 338, x1, x2, y1, y2)
            self.init_oar_count = cppCellModel.OARCellCount()
        else:
            self.controller_capsule = cppCellModel.controller_constructor(50, 50, 100, 350)
            self.init_hcell_count = cppCellModel.HCellCount()
        if mode == -1:
            self.verbose = False
        else :
            self.verbose = True
        self.total_dose = 0
        return self.observe()
    
    def act(self, action):
        dose = action / 2 if self.action_type == 'DQN' else action[0] * 4 + 1
        rest = 24 if self.action_type == 'DQN' else int(round(action[1] * 60 + 12))
        if self.dose_map is not None:
            tumor_radius = cppCellModel.tumor_radius(self.controller_capsule)
        pre_hcell = cppCellModel.HCellCount()
        pre_ccell = cppCellModel.CCellCount()
        pre_oar_cell = cppCellModel.OARCellCount()
        self.total_dose += dose
        if self.center:
            if self.tumor_radius:
                cppCellModel.irradiate_center_radius(self.controller_capsule, dose, action[2] * 25)
            else:
                cppCellModel.irradiate_center(self.controller_capsule, dose)
        else:
            if self.tumor_radius:
                cppCellModel.irradiate_radius(self.controller_capsule, dose, action[2] * 25)
            else:
                cppCellModel.irradiate(self.controller_capsule, dose)

        if self.dose_map is not None:
            self.add_radiation(dose, tumor_radius, cppCellModel.get_center_x(self.controller_capsule), cppCellModel.get_center_y(self.controller_capsule))
            self.dataset[0].append(cppCellModel.controllerTick(self.controller_capsule))
            self.dataset[1].append((pre_ccell, cppCellModel.CCellCount()))
            self.dataset[2].append(dose)
        cppCellModel.go(self.controller_capsule, rest)
        post_hcell = cppCellModel.HCellCount()
        post_ccell = cppCellModel.CCellCount()
        post_oar_cell = cppCellModel.OARCellCount()


        if self.verbose:
            if self.reward != 'oar':
                print("Radiation dose :", dose, "Gy ",
                "remaining :", post_ccell,  "time =", rest)
            else:
                print("Radiation dose :", dose, "Gy ",
                      "remaining :", post_ccell, "time =", rest, "radius =", cppCellModel.tumor_radius(self.controller_capsule))
        
        return self.adjust_reward(dose, post_ccell - pre_ccell, post_hcell - pre_hcell, post_oar_cell - pre_oar_cell)

    def adjust_reward(self, dose, ccell_killed, hcell_lost, oar_lost): 
        if self.special_reward and self.inTerminalState():
            if self.end_type == "L" or self.end_type == "T":
                return -1
            else:
                if self.reward == 'oar':
                    return cppCellModel.OARCellCount() / self.init_oar_count
                elif self.reward == 'dose':
                    return min((cppCellModel.HCellCount() / self.init_hcell_count), 1.0) - dose / 50
                else:
                    return 1
        else:
            if self.reward == 'dose' or self.reward == 'oar':
                return - dose / 50
            elif self.reward == 'killed':
                return (ccell_killed - 3 * hcell_lost)/50000

    def inTerminalState(self):
        if cppCellModel.CCellCount() <= 0 :
            if self.verbose:
                print("No more cancer")
            self.end_type = 'W'
            return True
        elif cppCellModel.HCellCount() < 10:
            if self.verbose:
                print("Cancer wins")
            self.end_type = "L"
            return True
        elif cppCellModel.controllerTick(self.controller_capsule) > 1550:
            if self.verbose:
                print("Time out!")
            self.end_type = "T"
            return True
        else:
            return False

    def nActions(self):
        if self.action_type == 'DQN':
            return 9
        elif self.action_type == 'AC':
            return [[0, 1], [0, 1], [0, 1]] if self.tumor_radius else [[0, 1], [0, 1]]

 
    def end(self):
        cppCellModel.delete_controller(self.controller_capsule)

    def inputDimensions(self):
        if self.resize:
            tab = [(1, 25, 25)]
        else:
            tab = [(1, 50, 50)]
        return tab

    def observe(self):
        if self.obs_type == 'types':
            cells = (np.array(cppCellModel.observeGrid(self.controller_capsule), dtype=np.float32) + 10.0) / 2.0
        else:
            cells = (np.array(cppCellModel.observeType(self.controller_capsule), dtype=np.float32) + 1.0) / 2.0 #  Obs from 0 to 1
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
                to_ret[i][j][2] = 255
            elif head[i][j] == -1:
                to_ret[i][j][0] = 255
    return to_ret


def conv(rad, x):
    #denom = 5.6568
    return math.erf((rad - x) / denom) - math.erf((-rad - x) / denom)


def tcp_test(num):
    count_failed = 0
    count_success = 0
    steps = []
    counts = []
    for i in range(num):
        print(i)
        controller = cppCellModel.controller_constructor(50, 50, 100, 350)
        counts.append(cppCellModel.HCellCount())
        for i in range(35):
            cppCellModel.irradiate(controller, 2)
            cppCellModel.go(controller, 24)
            if cppCellModel.CCellCount() == 0:
                steps.append(i + 1)
                break
        count = cppCellModel.CCellCount()
        if count > 10:
            count_failed += 1
        elif count == 0:
            count_success += 1
        counts[-1] /= cppCellModel.HCellCount()
        cppCellModel.delete_controller(controller)
    print("Percentage of full recovs :", (100*count_success)/ num)
    print("Percentage of almost recovs :", (100*(num - count_failed))/ num)
    print("Average dose in successes :", 2*sum(steps)/len(steps))
    print(sum(counts) / len(counts))


if __name__ == '__main__':
    tcp_test(200)
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use("TkAgg")
    plt.ion()

    controller = cppCellModel.controller_constructor(50,50,100,350)

    fig, axs = plt.subplots(2,2, constrained_layout=True)
    fig.suptitle('Cell proliferation at t = 0')
    glucose_plot = axs[0][0]
    glucose_plot.set_title('Glucose density')
    cell_plot = axs[1][0]
    cell_plot.set_title('Types of cells')
    oxygen_plot = axs[0][1]
    oxygen_plot.set_title('Oxygen density')
    cancer_count_plot = axs[1][1]
    cancer_count_plot.set_title('Number of cancer cells')
    ccount_ticks = []
    ccount_vals = []

    glucose_plot.imshow(cppCellModel.observeGlucose(controller))
    oxygen_plot.imshow(cppCellModel.observeOxygen(controller))
    cell_plot.imshow(cppCellModel.observeGrid(controller))
    ccount_ticks.append(cppCellModel.controllerTick(controller))
    ccount_vals.append(cppCellModel.CCellCount())
    cancer_count_plot.plot(ccount_ticks, ccount_vals)
    print(cppCellModel.CCellCount())
    for i in range(200):
        cppCellModel.go(controller, 12)
        if i % 2 == 0:
            cppCellModel.irradiate(controller, 2.0)
        fig.suptitle('Cell proliferation at t = ' + str((i+1)*12))
        glucose_plot.imshow(cppCellModel.observeGlucose(controller))
        oxygen_plot.imshow(cppCellModel.observeOxygen(controller))
        cell_plot.imshow(transform(cppCellModel.observeType(controller)))
        ccount_ticks.append(cppCellModel.controllerTick(controller))
        ccount_vals.append(cppCellModel.CCellCount())
        cancer_count_plot.plot(ccount_ticks, ccount_vals)
        plt.pause(0.02)

    cppCellModel.delete_controller(controller)

