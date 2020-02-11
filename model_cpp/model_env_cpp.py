import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import cv2
try:
    import cppModel
except:
    strErr = "\n\n`cppModel` module not found, "
    raise RuntimeError(strErr)

from deer.base_classes import Environment

class CellEnvironment(Environment):
    def __init__(self):
        self.controller_capsule = cppModel.controller_constructor(50, 50, 50, 350)
    
    def reset(self, mode):
        if mode == -1 or True:
            cppModel.delete_controller(self.controller_capsule)
            self.controller_capsule = cppModel.controller_constructor(50, 50, 50, 350)
    
    def act(self, action):
        pre_hcell = cppModel.HCellCount()
        pre_ccell = cppModel.CCellCount()
        cppModel.irradiate(self.controller_capsule, action / 2)
        cppModel.go(self.controller_capsule, 24)
        post_hcell = cppModel.HCellCount()
        post_ccell = cppModel.CCellCount()
        print("Radiation dose :", action / 2, "Gy ",
              "remaining :", post_ccell,  "time =", 24)
        if self.inTerminalState():
            if post_ccell > 0 :
                return -1
            elif cppModel.controllerTick(self.controller_capsule) > 2000:
                return -0.5
            else:
                return 1
        return self.adjust_reward(pre_ccell - post_ccell, pre_hcell-post_hcell)

    def adjust_reward(self, ccell_killed, hcell_lost): 
        return (ccell_killed - 5 * hcell_lost)/1000

    def inTerminalState(self):
        if cppModel.CCellCount() <= 0 :
            #print("No more cancer, healthy cells lost = ", self.h_cell_reset - HealthyCell.cell_count)
            return True
        elif cppModel.HCellCount() < 10:
            #print("Cancer wins, healthy cells lost = ",  self.h_cell_reset - HealthyCell.cell_count)
            return True
        elif cppModel.controllerTick(self.controller_capsule) > 2000:
            return True
        else:
            return False

    def nActions(self):
        return 9
 
    def end(self):
        cppModel.delete_controller(self.controller_capsule)

    def inputDimensions(self):
        return [(1, 25, 25)]

    def observe(self):
        cell_types = np.array(cppModel.observeGrid(self.controller_capsule), dtype=np.float32)
        return [cv2.resize(cell_types, dsize=(25,25), interpolation=cv2.INTER_CUBIC)]

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use("TkAgg")
    plt.ion()
    controller = cppModel.controller_constructor(50,50,50,0)
    fig, axs = plt.subplots(2,2, constrained_layout=True)
    fig.suptitle('Cell proliferation at t = 0')
    glucose_plot = axs[0][0]
    glucose_plot.set_title('Glucose density')
    cell_plot = axs[1][0]
    cell_plot.set_title('Types of cells')
    oxygen_plot = axs[0][1]
    oxygen_plot.set_title('Oxygen density')

    glucose_plot.imshow(cppModel.observeGlucose(controller))
    oxygen_plot.imshow(cppModel.observeOxygen(controller))
    cell_plot.imshow(cppModel.observeGrid(controller))

    for i in range(200):
        cppModel.go(controller, 12)
        if i > 30 and i % 2 == 0:
            cppModel.irradiate(controller, 3.0)
        fig.suptitle('Cell proliferation at t = ' + str((i+1)*12))
        glucose_plot.imshow(cppModel.observeGlucose(controller))
        oxygen_plot.imshow(cppModel.observeOxygen(controller))
        cell_plot.imshow(cppModel.observeGrid(controller))
        plt.pause(0.02)
    cppModel.delete_controller(controller)
