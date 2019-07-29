from cell_environment import CellEnvironment
import numpy as np
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
from deer.learning_algos.AC_net_keras import MyACNetwork
import deer.experiment.base_controllers as bc
from deer.policies import EpsilonGreedyPolicy
import sys
env = CellEnvironment()

rng = np.random.RandomState(123456)

# TODO : best algorithm, hyperparameter tuning
if sys.argv[1] == 'Q':
    network = MyQNetwork(
        environment=env,
        batch_size=8,
        random_state=rng)
else:
     network = MyACNetwork(
        environment=env,
        batch_size=8,
        random_state=rng)
'''
train_pol = EpsilonGreedyPolicy(
    Qnetwork,
    9,
    rng,
    0.32
)
'''
agent = NeuralAgent(
    env,
    network,
    #train_policy=train_pol,
    batch_size=8,
    random_state=rng)

agent.setDiscountFactor(0.95)
agent.attach(bc.VerboseController())
agent.attach(bc.InterleavedTestEpochController(
    epoch_length=500,
    controllers_to_disable=[0, 1]))
agent.setNetwork(sys.argv[2])
agent.run(n_epochs=2, epoch_length=1)