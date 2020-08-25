#!/usr/bin/env python3

import argparse
import datetime
print(datetime.datetime.now())
parser = argparse.ArgumentParser(description='Start training of an agent')
parser.add_argument('-s', '--simulation', choices=['py', 'c++'], dest="simulation", default='c++')
parser.add_argument('--obs_type', choices=['densities', 'segmentation'], default='densities')
parser.add_argument('--resize', action='store_true')
parser.add_argument('-t', action='store_true', dest='tumor_radius')
parser.add_argument('-n', '--network', choices=['DDPG', 'DQN'], dest='network', required=True)
parser.add_argument('-r', '--reward', choices=['dose', 'killed', 'oar'], dest='reward', required=True)
parser.add_argument('--no_special', action='store_false', dest='special')
parser.add_argument('--fname', default='nnet')
parser.add_argument('-c', '--center', action='store_true')
args = parser.parse_args()
print(args)

if args.simulation == 'c++':
    from model_cpp.model_env_cpp import CellEnvironment, transform, transform_densities
elif args.simulation == 'py':
    from cell_environment import CellEnvironment, transform, transform_densities

import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import numpy as np
from draw_treatment import make_img, make_img3
env = CellEnvironment(args.obs_type, args.resize, args.reward, args.network, args.special)

def save_tumor_image(data, tick):
    data = transform_densities(data)
    sizes = np.shape(data)
    fig = plt.figure()
    fig.set_size_inches(1. * sizes[0] / sizes[1], 1, forward = False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(data)
    plt.savefig('tmp/t'+str(tick), dpi=500)
    plt.close()

def save_dose_map(data, tick):
    pos = plt.imshow(data, vmin=0, vmax=70, cmap=mcol.LinearSegmentedColormap.from_list("MyCmapName", [[0, 0, 0.6], "r"]))
    cb = plt.colorbar(pos, ticks=[0, 35, 70])
    cb.set_label(label='[Gy]', size='large', weight='bold')
    cb.ax.tick_params(labelsize='large')
    plt.axis('off')
    plt.tight_layout(pad=0.05)
    plt.savefig('tmp/d'+str(tick))
    plt.close()

class EmpiricalTreatmentAgent():
    def __init__(self, env):
        self.env = env
        self.num_episodes = 0
        self.total_score = 0

    def summarizeTestPerformance(self):
        print("Episodes :", self.num_episodes, "Average score :", self.total_score/self.num_episodes)

    def _runEpisode(self, steps):
        self.num_episodes += 1
        i = 0
        env.reset(-1)

        while(not env.inTerminalState()):
            if i < 4:
                self.total_score += env.act(8)
                i += 1
            else:
                self.total_score += env.act(4)


from deer.agent import NeuralAgent
from deer.learning_algos.q_net_keras import MyQNetwork
from deer.learning_algos.AC_net_keras import MyACNetwork
import deer.experiment.base_controllers as bc
from deer.policies import EpsilonGreedyPolicy
from other_controllers import GaussianNoiseController, GridSearchController
from GaussianNoiseExplorationPolicy import GaussianNoiseExplorationPolicy

rng = np.random.RandomState(123456)

# TODO : best algorithm, hyperparameter tuning
if args.network == 'DQN':
    network = MyQNetwork(
        environment=env,
        batch_size=32,
        double_Q=True,
        random_state=rng)
elif args.network == 'DDPG':
    network = MyACNetwork(
        environment=env,
        batch_size=32,
        random_state=rng)

agent = NeuralAgent(
        env,
        network,
        train_policy=EpsilonGreedyPolicy(network, env.nActions(), rng, 0.0),
        replay_memory_size=1000,
        batch_size=32,
        random_state=rng)

#agent.attach(bc.VerboseController())
agent.setNetwork(args.fname)

#agent = EmpiricalTreatmentAgent(env)
count = 0
length_success = 0
avg_rad = 0
avg_h_cell_killed = 0
avg_percentage = 0
avg_doses = 0
k = 500
for i in range(k):
    print(i)
    agent._runEpisode(100000)
    if env.end_type == 'W':
        count += 1
        length_success += env.get_tick() - 350
        avg_rad += env.total_dose
        avg_percentage += env.surviving_fraction()
        avg_h_cell_killed += env.radiation_h_killed
        avg_doses += env.num_doses

print("TCP = ", count / k)
print("Avg rad", avg_rad / count)
print("Avg length in successes", length_success / count)
print("Avg number of doses", avg_doses / count)
print("Avg hcells killed", avg_h_cell_killed / count)
print("Avg surviving fraction: ", avg_percentage / count)
#agent.summarizeTestPerformance()
env.init_dataset()
env.init_dose_map()
agent._runEpisode(100000)
#env.show_dose_map()
print("done")


save_tumor_image(env.tumor_images[0][1], env.tumor_images[0][0])
save_dose_map(env.dose_maps[0][1], env.dose_maps[0][0])
save_tumor_image(env.tumor_images[int(len(env.tumor_images) / 2)][1], env.tumor_images[int(len(env.tumor_images) / 2)][0])
save_dose_map(env.dose_maps[int(len(env.tumor_images) / 2)][1], env.dose_maps[int(len(env.tumor_images) / 2)][0])
#save_tumor_image(env.tumor_images[int(len(env.tumor_images) * 2 / 3)][1], env.tumor_images[int(len(env.tumor_images) * 2 / 3)][0])
#save_dose_map(env.dose_maps[int(len(env.tumor_images) * 2 / 3)][1], env.dose_maps[int(len(env.tumor_images) * 2 / 3)][0])
save_tumor_image(env.tumor_images[-1][1], env.tumor_images[-1][0])
save_dose_map(env.dose_maps[-1][1], env.dose_maps[-1][0])
ticks = [env.tumor_images[0][0], env.tumor_images[int(len(env.tumor_images) / 2)][0], env.tumor_images[-1][0]]
make_img3(ticks, args.fname)


ticks, counts, doses = env.dataset
fig, ax1 = plt.subplots()

color = 'tab:orange'
ax1.set_xlabel('time (h)')
ax1.set_ylabel('Dose (Gy)', color=color)
ax1.set_ylim(0, 5)
ax1.set_xlim(0, 450)
ax1.plot(ticks, doses, color=color, marker='o', mew=8, linewidth=4)
ax1.tick_params(axis='y', labelcolor=color)
d_ticks = []
d_counts = []
for i in range(len(ticks)):
    d_ticks += [ticks[i], ticks[i]]
    d_counts += [counts[i][0], counts[i][1]]

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.savefig('tmp/'+args.fname+'_treat')


print(ticks, doses)

doses_data = np.zeros((100, 100), dtype=float)
for i in range(100):
    env.init_dataset()
    agent._runEpisode(100000)
    _, _, doses = env.dataset
    doses_data[i, :len(doses)] = doses

print(np.mean(doses_data, 0))
print(np.std(doses_data, 0))

env.end()
