import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import cv2
try:
    import cppCellModel
except:
    strErr = "\n\n`cppCellModel` module not found, "
    raise RuntimeError(strErr)

from deer.base_classes import Environment

class CellEnvironment(Environment):
    def __init__(self):
        self.controller_capsule = cppCellModel.controller_constructor(50, 50, 50, 350)
    
    def reset(self, mode):
        cppCellModel.delete_controller(self.controller_capsule)
        self.controller_capsule = cppCellModel.controller_constructor(50, 50, 50, 350)
        if mode == -1:
            self.verbose = False
        else :
            self.verbose = True
            
    
    def act(self, action):
        pre_hcell = cppCellModel.HCellCount()
        pre_ccell = cppCellModel.CCellCount()
        cppCellModel.irradiate(self.controller_capsule, action / 2)
        cppCellModel.go(self.controller_capsule, 24)
        post_hcell = cppCellModel.HCellCount()
        post_ccell = cppCellModel.CCellCount()
        if self.verbose:
            print("Radiation dose :", action / 2, "Gy ",
              "remaining :", post_ccell,  "time =", 24)
        if self.inTerminalState():
            if post_ccell > 0 :
                return -1
            elif cppCellModel.controllerTick(self.controller_capsule) > 2000:
                return -0.5
            else:
                return 1
        return self.adjust_reward(pre_ccell - post_ccell, pre_hcell-post_hcell)

    def adjust_reward(self, ccell_killed, hcell_lost): 
        return (ccell_killed - 5 * hcell_lost)/1000

    def inTerminalState(self):
        if cppCellModel.CCellCount() <= 0 :
            #print("No more cancer, healthy cells lost = ", self.h_cell_reset - HealthyCell.cell_count)
            return True
        elif cppCellModel.HCellCount() < 10:
            #print("Cancer wins, healthy cells lost = ",  self.h_cell_reset - HealthyCell.cell_count)
            return True
        elif cppCellModel.controllerTick(self.controller_capsule) > 2000:
            return True
        else:
            return False

    def nActions(self):
        return 9
 
    def end(self):
        cppCellModel.delete_controller(self.controller_capsule)

    def inputDimensions(self):
        return [(1, 25, 25)]

    def observe(self):
        cell_types = np.array(cppCellModel.observeGrid(self.controller_capsule), dtype=np.float32)
        return [cv2.resize(cell_types, dsize=(25,25), interpolation=cv2.INTER_CUBIC)]

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use("TkAgg")
    plt.ion()
    controller = cppCellModel.controller_constructor_oar(50,50,50,0, 5,15,5,15)
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

    for i in range(200):
        cppCellModel.go(controller, 12)
        if i > 30 and i % 2 == 0:
            cppCellModel.irradiate(controller, 3.0)
        fig.suptitle('Cell proliferation at t = ' + str((i+1)*12))
        glucose_plot.imshow(cppCellModel.observeGlucose(controller))
        oxygen_plot.imshow(cppCellModel.observeOxygen(controller))
        cell_plot.imshow(cppCellModel.observeGrid(controller))
        ccount_ticks.append(cppCellModel.controllerTick(controller))
        ccount_vals.append(cppCellModel.CCellCount())
        cancer_count_plot.plot(ccount_ticks, ccount_vals)
        plt.pause(0.02)
    cppCellModel.delete_controller(controller)
