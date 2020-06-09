#!/usr/bin/env python3

import argparse
import datetime
print(datetime.datetime.now())
parser = argparse.ArgumentParser(description='Start training of an agent')
parser.add_argument('--canicula', action='store_true')
parser.add_argument('-s', '--simulation', choices=['py', 'c++'], dest="simulation", default='c++')
parser.add_argument('--obs_type', choices=['head', 'types'], default='types')
parser.add_argument('--resize', action='store_true')
parser.add_argument('-t', action='store_true', dest='tumor_radius')
parser.add_argument('-n', '--network', choices=['AC', 'DQN'], dest='network', required=True)
parser.add_argument('-r', '--reward', choices=['dose', 'killed', 'oar'], dest='reward', required=True)
parser.add_argument('--no_special', action='store_false', dest='special')
parser.add_argument('-l', '--learning_rate', nargs=3, type=float, default=[0.001, 0.8,1])
parser.add_argument('--fname', default='nnet')
parser.add_argument('-e', '--epochs', nargs=2, type=int, default=[20, 2500])
parser.add_argument('-c', '--center', action='store_true')
args = parser.parse_args()
print(args)

if args.simulation == 'c++':
    from model_cpp.model_env_cpp import CellEnvironment, transform
elif args.simulation == 'py':
    from cell_environment import CellEnvironment

import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import numpy as np
from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
from deer.learning_algos.AC_net_keras import MyACNetwork
import deer.experiment.base_controllers as bc
from deer.policies import EpsilonGreedyPolicy
from other_controllers import GaussianNoiseController, GridSearchController
from GaussianNoiseExplorationPolicy import GaussianNoiseExplorationPolicy
env = CellEnvironment(args.obs_type, args.resize, args.reward, args.network, args.tumor_radius, args.special, args.center)

class EmpiricalTreatmentAgent():
    def __init__(self, env):
        self.env = env
        self.num_episodes = 0
        self.total_score = 0

    def average_score(self):
        print("Episodes :", self.num_episodes, "Average score :", self.total_score/self.num_episodes)

    def _runEpisode(self, steps):
        self.num_episodes += 1
        i = 0
        env.reset(-1)

        self.total_score += env.act(8)
        self.total_score += env.act(8)
        self.total_score += env.act(8)
        while(not env.inTerminalState()):
            if i < 35 or True:
                self.total_score += env.act(4)
                i += 1
            else:
                self.total_score += env.act(0)



'''
rng = np.random.RandomState(123456)

# TODO : best algorithm, hyperparameter tuning
if args.network == 'DQN':
    network = MyQNetwork(
        environment=env,
        batch_size=32,
        freeze_interval=args.epochs[1],
        double_Q=True,
        random_state=rng)
elif args.network == 'AC':
    network = MyACNetwork(
        environment=env,
        batch_size=32,
        freeze_interval=args.epochs[1],
        random_state=rng)

agent = NeuralAgent(
        env,
        network,
        train_policy=EpsilonGreedyPolicy(network, env.nActions(), rng, 0.0),
        replay_memory_size=args.epochs[0]*args.epochs[1] * 2,
        batch_size=32,
        random_state=rng)

#agent.attach(bc.VerboseController())
agent.setNetwork(args.fname)
'''
agent = EmpiricalTreatmentAgent(env)
count = 0
length_success = 0
avg_rad = 0
avg_h_cell_killed = 0
k = 100
for i in range(k):
    print(i)
    agent._runEpisode(100000)
    if env.end_type == 'W':
        count += 1
        length_success += env.get_tick() - 350
    avg_rad += env.total_dose
    avg_h_cell_killed += env.radiation_h_killed

print("TCP = ", count / k)
print("Avg rad", avg_rad / k)
print("Avg length in successes", length_success / count)
print("Avg hcells killed", avg_h_cell_killed / k)
agent.average_score()
"""
env.init_dose_map()
agent._runEpisode(100000)
#env.show_dose_map()
print("done")


fig, axs = plt.subplots(4, 2, constrained_layout=True)
axs[0][0].set_title("Tumor at time:"+ str(env.tumor_images[0][0]))
axs[0][0].imshow(transform(env.tumor_images[0][1]))
axs[0][0].set_axis_off()
axs[0][1].set_title("Dose map at time: "+str(env.dose_maps[0][0]))
p = axs[0][1].imshow(env.dose_maps[0][1], vmin=0, vmax=70, cmap=mcol.LinearSegmentedColormap.from_list("MyCmapName",[[0,0,0.6],"r"]))
#fig.colorbar(p, ax=axs[0][1])
axs[0][1].set_axis_off()

axs[1][0].set_title("Tumor at time:"+ str(env.tumor_images[int(len(env.tumor_images) / 3)][0]))
axs[1][0].imshow(transform(env.tumor_images[int(len(env.tumor_images) / 3)][1]))
axs[1][0].set_axis_off()
axs[1][1].set_title("Dose map at time: "+str(env.dose_maps[int(len(env.tumor_images) / 3)][0]))
axs[1][1].imshow(env.dose_maps[int(len(env.tumor_images) / 3)][1], vmin=0, vmax=70,  cmap=mcol.LinearSegmentedColormap.from_list("MyCmapName",[[0,0,0.6],"r"]))
axs[1][1].set_axis_off()

axs[2][0].set_title("Tumor at time:"+ str(env.tumor_images[int(len(env.tumor_images) * 2 / 3)][0]))
axs[2][0].imshow(transform(env.tumor_images[int(len(env.tumor_images) * 2 / 3)][1]))
axs[2][0].set_axis_off()
axs[2][1].set_title("Dose map at time: "+str(env.dose_maps[int(len(env.tumor_images) * 2 / 3)][0]))
axs[2][1].imshow(env.dose_maps[int(len(env.tumor_images) * 2 / 3)][1], vmin=0, vmax=70, cmap=mcol.LinearSegmentedColormap.from_list("MyCmapName",[[0,0,0.6],"r"]))
axs[2][1].set_axis_off()

axs[3][0].set_title("Tumor at time:"+ str(env.tumor_images[-1][0]))
axs[3][0].imshow(transform(env.tumor_images[-1][1]))
axs[3][0].set_axis_off()
axs[3][1].set_title("Dose map at time: "+str(env.dose_maps[-1][0]))
axs[3][1].imshow(env.dose_maps[-1][1], vmin=0, vmax=70, cmap=mcol.LinearSegmentedColormap.from_list("MyCmapName",[[0,0,0.6],"r"]))
axs[3][1].set_axis_off()

ticks, counts, doses = env.dataset
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time (h)')
ax1.set_ylabel('Dose (Gy)', color=color)
ax1.set_ylim(0, 5)
ax1.plot(ticks, doses, color=color, marker='o')
ax1.tick_params(axis='y', labelcolor=color)
d_ticks = []
d_counts = []
for i in range(len(ticks)):
    d_ticks += [ticks[i], ticks[i]]
    d_counts += [counts[i][0], counts[i][1]]
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('Number of cancer cells (log)', color=color)  # we already handled the x-label with ax1
ax2.set_ybound(0, 10000)
ax2.plot(d_ticks, d_counts, color=color)
ax2.set_yscale('log')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
"""
env.end()

