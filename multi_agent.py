from cell_environment import CellEnvironment
from deer.base_classes import Environment
from model.cell import CancerCell, HealthyCell, OARCell
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
import numpy as np
import deer.experiment.base_controllers as bc

class MultiAgentEnvironment(CellEnvironment):
    def __init__(self):
        self.dose_agent = None
        self.hour_agent = None
        self.rest = 0
        self.dose = 0
        self.dose_training = False
        self.hour_training = False

    def set_hour_agent(self, hour_agent):
        self.hour_agent = hour_agent

    def set_dose_agent(self, dose_agent):
        self.hour_agent = dose_agent

    def act(self, action):
        pre_hcell = HealthyCell.cell_count
        pre_ccell = CancerCell.cell_count
        pre_oarcell = OARCell.cell_count
        self.base_env.current_controller.grid.irradiate(1+(action/2), 25, 25)
        if (self.hour_agent):
            self.hour_agent.dose = 1+(action/2)
            self.rest = (self.hour_agent._chooseAction()[0] +1)*12
        else:
            self.rest = self.base_env.rand_time
        for _ in range(self.rest):
            self.base_env.current_controller.go()
        post_hcell = HealthyCell.cell_count
        post_ccell = CancerCell.cell_count
        post_oarcell = OARCell.cell_count
        print("Radiation dose :", 1 + (action / 2), "Gy", (pre_ccell - post_ccell), "Cancer cell killed",
              CancerCell.cell_count, "remaining", "time =", self.rest)
        return (post_hcell-pre_hcell)/1000