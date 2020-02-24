#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Start training of an agent')
parser.add_argument('--canicula', action='store_true')
parser.add_argument('-s', '--simulation', choices=['py', 'c++'], dest="simulation", default='py')
parser.add_argument('--obs_type', choices=['head', 'types'], default='types')
parser.add_argument('--resize', action='store_true')
parser.add_argument('-t', action='store_true', dest='tumor_radius')
parser.add_argument('-n', '--network', choices=['AC', 'DQN'], dest='network', required=True)
parser.add_argument('-r', '--reward', choices=['dose', 'killed', 'oar'], dest='reward', required=True)
parser.add_argument('--no_special', action='store_false', dest='special')
parser.add_argument('-l', '--learning_rate', nargs=3, type=float)

args = parser.parse_args()
print(args)
if args.canicula:
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = '2'  # GPU cluster
if args.simulation == 'c++':
    from model_cpp.model_env_cpp import CellEnvironment
elif args.simulation == 'py':    
    from cell_environment import CellEnvironment


import numpy as np
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
from deer.learning_algos.AC_net_keras import MyACNetwork
import deer.experiment.base_controllers as bc
from deer.policies import EpsilonGreedyPolicy
env = CellEnvironment(args.obs_type, args.resize, args.reward, args.network, args.tumor_radius, args.special)

rng = np.random.RandomState(123456)

# TODO : best algorithm, hyperparameter tuning
if args.network == 'DQN':
    network = MyQNetwork(
        environment=env,
        batch_size=32,
        random_state=rng)
    agent = NeuralAgent(
        env,
        network,
        batch_size=32,
        random_state=rng)
    agent.setDiscountFactor(0.95)
    agent.attach(bc.VerboseController())
    agent.attach(bc.TrainerController())
    agent.attach(bc.EpsilonController(initial_e=0.8, e_decays=100000, e_min=0.01))
    agent.attach(bc.LearningRateController(args.learning_rate[0], args.learning_rate[1], args.learning_rate[2]))
    agent.attach(bc.InterleavedTestEpochController(
    epoch_length=100,
    controllers_to_disable=[0, 1, 2, 3]))
elif args.network == 'AC':
    network = MyACNetwork(
        environment=env,
        batch_size=32,
        random_state=rng)
    agent = NeuralAgent(
        env,
        network,
        batch_size=32,
        random_state=rng)
    agent.setDiscountFactor(0.95)
    agent.attach(bc.VerboseController())
    agent.attach(bc.TrainerController())
    # agent.attach(bc.EpsilonController(initial_e=0.8, e_decays=100000, e_min=0.01))
    agent.attach(bc.LearningRateController(args.learning_rate[0], args.learning_rate[1], args.learning_rate[2]))
    agent.attach(bc.InterleavedTestEpochController(
        epoch_length=100,
        controllers_to_disable=[0, 1, 2, 3]))




agent.attach(bc.FindBestController(validationID=0, testID=0, unique_fname='nnet'))
agent.run(n_epochs=100, epoch_length=1000)
