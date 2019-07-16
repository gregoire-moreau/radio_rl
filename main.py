from cell_environment import CellEnvironment
import numpy as np
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
from deer.learning_algos.AC_net_keras import MyACNetwork
import deer.experiment.base_controllers as bc

env = CellEnvironment()

rng = np.random.RandomState(123456)

# TODO : best algorithm, hyperparameter tuning
Qnetwork = MyACNetwork(
    environment=env,
    random_state=rng)


agent = NeuralAgent(
    env,
    Qnetwork,
    random_state=rng)

# TODO : Find best discount factor
agent.setDiscountFactor(0.9)
agent.attach(bc.VerboseController())

agent.attach(bc.TrainerController())

agent.attach(bc.InterleavedTestEpochController(
    epoch_length=500,
    controllers_to_disable=[0, 1]))

# --- Run the experiment ---
agent.run(n_epochs=100, epoch_length=1000)

agent.dumpNetwork("net")