from cell_environment import CellEnvironment
from deer.base_classes import Environment
from model.cell import CancerCell, HealthyCell, OARCell
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
import numpy as np
import deer.experiment.base_controllers as bc

class DoseAgentEnvironment(Environment):

    def __init__(self, base_env):
        self.base_env = base_env
        self.hour_agent = None
        self.rest = 0

    def set_hour_agent(self, hour_agent):
        self.hour_agent = hour_agent

    def reset(self, mode):
        self.base_env.reset(mode)

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

    def inTerminalState(self):
        return self.base_env.inTerminalState()

    def nActions(self):
        return 9

    def end(self):
        del self.base_env

    def inputDimensions(self):
        return self.base_env.inputDimensions()

    def observe(self):
        obs = self.base_env.observe()
        obs[0] = self.rest
        return obs

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)


class HourAgentEnvironment(Environment):

    def __init__(self, base_env):
        self.base_env = base_env
        self.dose_agent = None
        self.dose = 0

    def set_dose_agent(self, dose_agent):
        self.dose_agent = dose_agent

    def reset(self, mode):
        self.base_env.reset(mode)

    def act(self, action):
        pre_hcell = self.pre_hcell
        pre_ccell = self.pre_ccell
        pre_oarcell = OARCell.cell_count
        #self.base_env.current_controller.grid.irradiate(2, 25, 25)
        # self.current_controller.grid.irradiate(1+(action/2), 25, 25)

        for _ in range((action+1)*12):
            self.base_env.current_controller.go()
        self.dose_agent.rest = (action+1)*12
        post_hcell = HealthyCell.cell_count
        post_ccell = CancerCell.cell_count
        post_oarcell = OARCell.cell_count
        print("Radiation dose :", self.dose, "Gy", (pre_ccell - post_ccell), "Cancer cell killed",
              CancerCell.cell_count, "remaining", "time =", (action+1)*12)
        return (post_hcell - pre_hcell)/1000

    def inTerminalState(self):
        return self.base_env.inTerminalState()

    def nActions(self):
        return 6

    def end(self):
        del self.base_env

    def inputDimensions(self):
        return self.base_env.inputDimensions()

    def observe(self):
        self.pre_hcell = HealthyCell.cell_count
        self.pre_ccell = CancerCell.cell_count
        obs = self.base_env.observe()
        if self.dose == 0: #Hour agent is the agent currently being trained
            self.dose = self.dose_agent._chooseAction()[0]
            self.base_env.current_controller.grid.irradiate(self.dose, 25, 25)
        obs[0] = self.dose
        self.dose = 0
        return obs


    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)


env = CellEnvironment()
rng = np.random.RandomState(123456)
dose_env = DoseAgentEnvironment(env)
hour_env = HourAgentEnvironment(env)

Qnetwork_dose = MyQNetwork(
    environment=dose_env,
    batch_size=8,
    random_state=rng)

Qnetwork_hour = MyQNetwork(
    environment=hour_env,
    batch_size=8,
    random_state=rng)

agent_dose = NeuralAgent(
    dose_env,
    Qnetwork_dose,
    batch_size=8,
    random_state=rng)

agent_hour = NeuralAgent(
    hour_env,
    Qnetwork_hour,
    batch_size=8,
    random_state=rng)


agent_dose.setDiscountFactor(0.99)
agent_dose.attach(bc.VerboseController())
agent_dose.attach(bc.TrainerController())
agent_dose.attach(bc.EpsilonController(initial_e=0.8, e_decays=5000, e_min=0.))
agent_dose.attach(bc.LearningRateController(0.0001, 0.5, 1))
agent_dose.attach(bc.InterleavedTestEpochController(
    epoch_length=8,
    controllers_to_disable=[0, 1, 2,3]))
agent_dose.run(n_epochs=5, epoch_length=1000)
agent_dose.dumpNetwork("net_dose_1st_step", nEpoch = 5)

dose_env.set_hour_agent(agent_hour)
hour_env.set_dose_agent(agent_dose)


agent_hour.setDiscountFactor(0.99)
agent_hour.attach(bc.VerboseController())
agent_hour.attach(bc.TrainerController())
agent_hour.attach(bc.EpsilonController(initial_e=0.8, e_decays=5000, e_min=0.))
agent_hour.attach(bc.LearningRateController(0.0001, 0.5, 1))
agent_hour.attach(bc.InterleavedTestEpochController(
    epoch_length=8,
    controllers_to_disable=[0, 1, 2,3]))
agent_hour.run(n_epochs=5, epoch_length=1000)
agent_hour.dumpNetwork("net_hour_2nd_step", nEpoch = 5)

for _ in range(100):
    agent_dose.run(n_epochs=1, epoch_length=64)
    agent_hour.run(n_epochs=1, epoch_length=64)

agent_dose.dumpNetwork("net_dose_3rd_step", nEpoch = 5)
agent_hour.dumpNetwork("net_hour_3rd_step", nEpoch = 5)