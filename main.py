from cell_environment import CellEnvironment
import numpy as np
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
import deer.experiment.base_controllers as bc

env = CellEnvironment()

rng = np.random.RandomState(123456)

qnetwork = MyQNetwork(
    environment=env,
    random_state=rng)

agent = NeuralAgent(
    env,
    qnetwork,
    random_state=rng)

agent.attach(bc.VerboseController())

agent.attach(bc.TrainerController())

agent.attach(bc.InterleavedTestEpochController(
    epoch_length=500,
    controllers_to_disable=[0, 1]))

# --- Run the experiment ---
agent.run(n_epochs=100, epoch_length=1000)