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

    def set_hour_agent(self, hour_agent):
        self.hour_agent = hour_agent

    def reset(self, mode):
        self.base_env.reset(mode)

    def act(self, action):
        pre_hcell = HealthyCell.cell_count
        pre_ccell = CancerCell.cell_count
        pre_oarcell = OARCell.cell_count
        self.base_env.current_controller.grid.irradiate(1+(action/2), 25, 25)
        for _ in range(24):
            self.base_env.current_controller.go()
        post_hcell = HealthyCell.cell_count
        post_ccell = CancerCell.cell_count
        post_oarcell = OARCell.cell_count
        print("Radiation dose :", 1 + (action / 2), "Gy", (pre_ccell - post_ccell), "Cancer cell killed",
              CancerCell.cell_count, "remaining", "time =", 5)
        return 1000

    def inTerminalState(self):
        return self.base_env.inTerminalState()

    def nActions(self):
        return 9

    def end(self):
        del self.base_env

    def inputDimensions(self):
        return self.base_env.inputDimensions()

    def observe(self):
        return self.base_env.observe()

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        print(test_data_set)


class HourAgentEnvironment(Environment):

    def __init__(self, base_env):
        self.base_env = base_env

    def set_dose_agent(self, dose_agent):
        self.hour_agent = dose_agent

    def reset(self, mode):
        self.base_env.reset(mode)

    def act(self, action):
        pre_hcell = HealthyCell.cell_count
        pre_ccell = CancerCell.cell_count
        pre_oarcell = OARCell.cell_count
        self.base_env.current_controller.grid.irradiate(2, 25, 25)
        # self.current_controller.grid.irradiate(1+(action/2), 25, 25)

        for _ in range((action+1)*12):
            self.base_env.current_controller.go()
        post_hcell = HealthyCell.cell_count
        post_ccell = CancerCell.cell_count
        post_oarcell = OARCell.cell_count
        print("Radiation dose :", 2, "Gy", (pre_ccell - post_ccell), "Cancer cell killed",
              CancerCell.cell_count, "remaining", "time =", (action+1)*12)
        return 1000

    def inTerminalState(self):
        return self.base_env.inTerminalState()

    def nActions(self):
        return 9

    def end(self):
        del self.base_env

    def inputDimensions(self):
        return self.base_env.inputDimensions()

    def observe(self):
        return self.base_env.observe()

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

dose_env.set_hour_agent(agent_hour)
hour_env.set_dose_agent(agent_dose)

agent_dose.setDiscountFactor(0.99)
agent_dose.attach(bc.VerboseController())
agent_dose.attach(bc.TrainerController())
agent_dose.attach(bc.EpsilonController(initial_e=0.8, e_decays=5000, e_min=0.))
agent_dose.attach(bc.LearningRateController(0.0000000000000001, 0.5, 1))
agent_dose.attach(bc.InterleavedTestEpochController(
    epoch_length=8,
    controllers_to_disable=[0, 1, 2,3]))
agent_hour.setDiscountFactor(0.99)
agent_hour.attach(bc.VerboseController())
agent_hour.attach(bc.TrainerController())
agent_hour.attach(bc.EpsilonController(initial_e=0.8, e_decays=5000, e_min=0.))
agent_hour.attach(bc.LearningRateController(0.0000000000000001, 0.5, 1))
agent_hour.attach(bc.InterleavedTestEpochController(
    epoch_length=8,
    controllers_to_disable=[0, 1, 2,3]))

for _ in range(100):
    agent_dose.run(n_epochs=1, epoch_length=64)
    agent_hour.run(n_epochs=1, epoch_length=64)
