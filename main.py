#!/usr/bin/env python3

import argparse
import datetime
print(datetime.datetime.now())
parser = argparse.ArgumentParser(description='Start training of an agent')
parser.add_argument('--canicula', action='store_true')
parser.add_argument('-s', '--simulation', choices=['py', 'c++'], dest="simulation", default='c++')
parser.add_argument('--obs_type', choices=['segmentation', 'densities', 'scalars'], default='densities')
parser.add_argument('--resize', action='store_true')
parser.add_argument('-n', '--network', choices=['DDPG', 'DQN'], dest='network', required=True)
parser.add_argument('-r', '--reward', choices=['dose', 'killed', 'oar'], dest='reward', required=True)
parser.add_argument('--no_special', action='store_false', dest='special')
parser.add_argument('-l', '--learning_rate', nargs=3, type=float, default=[0.0001, 0.75,5])
parser.add_argument('--fname', default='nnet')
parser.add_argument('-e', '--epochs', nargs=2, type=int, default=[20, 2500])
parser.add_argument('--exploration', choices=['epsilon', 'gauss'], dest='exploration', default='epsilon')

args = parser.parse_args()
print(args)

if args.network == 'DQN' and args.exploration == 'gauss':
    raise Exception("Can't use Gaussian Noise with DQN")

if args.canicula:
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = '2'  # GPU cluster
if args.simulation == 'c++':
    from model_cpp.model_env_cpp import CellEnvironment
elif args.simulation == 'py':    
    from model.cell_environment import CellEnvironment


import numpy as np
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
from deer.learning_algos.AC_net_keras import MyACNetwork
import deer.experiment.base_controllers as bc
from deer.policies import EpsilonGreedyPolicy
from misc.other_controllers import GaussianNoiseController
from misc.GaussianNoiseExplorationPolicy import GaussianNoiseExplorationPolicy
env = CellEnvironment(args.obs_type, args.resize, args.reward, args.network, args.special)

rng = np.random.RandomState(777)

# TODO : best algorithm, hyperparameter tuning
if args.network == 'DQN':
    network = MyQNetwork(
        environment=env,
        batch_size=32,
        freeze_interval=args.epochs[1],
        double_Q=True,
        random_state=rng)
    agent = NeuralAgent(
        env,
        network,
        replay_memory_size=min(int(args.epochs[0]*args.epochs[1] * 1.1), 100000),
        batch_size=32,
        random_state=rng)
    agent.setDiscountFactor(0.95)
    agent.attach(bc.FindBestController(validationID=0, unique_fname=args.fname))
    agent.attach(bc.VerboseController())
    agent.attach(bc.TrainerController())
    agent.attach(bc.EpsilonController(initial_e=0.8, e_decays=args.epochs[0] * args.epochs[1], e_min=0.2))
    agent.attach(bc.LearningRateController(args.learning_rate[0], args.learning_rate[1], args.learning_rate[2]))
    agent.attach(bc.InterleavedTestEpochController(
    epoch_length=1000,
    controllers_to_disable=[1, 2, 3, 4]))
elif args.network == 'DDPG':
    network = MyACNetwork(
        environment=env,
        batch_size=32,
        double_Q=True,
        freeze_interval=args.epochs[1],
        random_state=rng)
    agent = NeuralAgent(
        env,
        network,
        train_policy=GaussianNoiseExplorationPolicy(network, env.nActions(), rng, .5) if args.exploration == 'gauss' else EpsilonGreedyPolicy(network, env.nActions(), rng, 0.1),
        replay_memory_size=min(args.epochs[0]*args.epochs[1] * 2, 100000),
        batch_size=32,
        random_state=rng)
    agent.setDiscountFactor(0.95)
    agent.attach(bc.FindBestController(validationID=0, unique_fname=args.fname))
    agent.attach(bc.VerboseController())
    agent.attach(bc.TrainerController())
    if args.exploration == 'gauss':
        agent.attach(GaussianNoiseController(initial_std_dev=0.5, n_decays=args.epochs[0] * args.epochs[1], final_std_dev=0.005))
    else:
        agent.attach(bc.EpsilonController(initial_e=0.8, e_decays=args.epochs[0] * args.epochs[1], e_min=0.05))
    agent.attach(bc.LearningRateController(args.learning_rate[0], args.learning_rate[1], args.learning_rate[2]))
    agent.attach(bc.InterleavedTestEpochController(
        epoch_length=1000,
        controllers_to_disable=[1, 2, 3, 4]))

agent.run(n_epochs=args.epochs[0], epoch_length=args.epochs[1])
