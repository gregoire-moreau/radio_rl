from model_cpp.model_env_cpp import CellEnvironment
import numpy as np
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
from deer.learning_algos.AC_net_keras import MyACNetwork
import deer.experiment.base_controllers as bc
from deer.policies import EpsilonGreedyPolicy
env = CellEnvironment()

rng = np.random.RandomState(123456)

# TODO : best algorithm, hyperparameter tuning
Qnetwork = MyQNetwork(
    environment=env,
    batch_size=32,
    random_state=rng)


agent = NeuralAgent(
    env,
    Qnetwork,
    batch_size=32,
    random_state=rng)

agent.setDiscountFactor(0.95)
agent.attach(bc.VerboseController())
agent.attach(bc.TrainerController())
agent.attach(bc.EpsilonController(initial_e=0.8, e_decays=100000, e_min=0.01))
agent.attach(bc.LearningRateController(0.001, 0.8, 5))
agent.attach(bc.InterleavedTestEpochController(
    epoch_length=100,
    controllers_to_disable=[0, 1, 2, 3]))
#agent.setNetwork("net_Q3", nEpoch=10)
agent.run(n_epochs=100, epoch_length=1000)
agent.dumpNetwork("net", nEpoch = 100)
