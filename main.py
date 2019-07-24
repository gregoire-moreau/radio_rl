from cell_environment import CellEnvironment
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
    batch_size=1,
    random_state=rng)


train_pol = EpsilonGreedyPolicy(
    Qnetwork,
    9,
    rng,
    0.8
)

agent = NeuralAgent(
    env,
    Qnetwork,
    batch_size=1,
    train_policy = train_pol,
    random_state=rng)

agent.setDiscountFactor(0.99)
agent.attach(bc.VerboseController())
agent.attach(bc.LearningRateController(0.00005, 0.5, 1))
agent.attach(bc.TrainerController())
agent.attach(bc.EpsilonController())
agent.attach(bc.InterleavedTestEpochController(
    epoch_length=500,
    controllers_to_disable=[0, 1]))

# --- Run the experiment ---
agent.run(n_epochs=100, epoch_length=1000)

agent.dumpNetwork("net")