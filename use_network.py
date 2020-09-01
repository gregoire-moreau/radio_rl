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
from treatment_var import treatment_var
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
            if i <35:
                self.total_score += env.act(2)
                i += 1
            else:
                self.total_score += env.act(2)


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
if args.fname == 'baseline':
    agent = EmpiricalTreatmentAgent(env)
else:
    agent.setNetwork(args.fname)

count = 0
length_success = []
avg_rad = []
avg_h_cell_killed = []
avg_percentage = []
avg_doses = []
k = 1000
for i in range(k):
    #print(i)
    agent._runEpisode(100000)
    if env.end_type == 'W':
        count += 1
    length_success.append(env.get_tick() - 350)
    avg_rad.append(env.total_dose)
    avg_percentage.append(env.surviving_fraction())
    avg_h_cell_killed.append(env.radiation_h_killed)
    avg_doses.append(env.num_doses)

rads = np.array(avg_rad)
percentages = np.array(avg_percentage)
fracs = np.array(avg_doses)
durations = np.array(length_success)

print("TCP = ", count / k)
print("Avg rad", np.mean(rads), "Std error:", np.std(rads))
print("Avg length in successes", np.mean(durations), "Std error:", np.std(durations))
print("Avg number of doses", np.mean(fracs), "Std error:", np.std(fracs))
#print("Avg hcells killed", avg_h_cell_killed / k)
print("Avg surviving fraction: ", np.mean(percentages), "Std error:", np.std(percentages))
#agent.summarizeTestPerformance()
env.init_dataset()
env.init_dose_map()
agent._runEpisode(100000)
#env.show_dose_map()
print("done")


save_tumor_image(env.tumor_images[0][1], env.tumor_images[0][0])
save_dose_map(env.dose_maps[0][1], env.dose_maps[0][0])
save_tumor_image(env.tumor_images[int(len(env.tumor_images) / 3)][1], env.tumor_images[int(len(env.tumor_images) / 3)][0])
save_dose_map(env.dose_maps[int(len(env.tumor_images) / 3)][1], env.dose_maps[int(len(env.tumor_images) / 3)][0])
save_tumor_image(env.tumor_images[int(len(env.tumor_images) / 2)][1], env.tumor_images[int(len(env.tumor_images) / 2)][0])
save_dose_map(env.dose_maps[int(len(env.tumor_images) / 2)][1], env.dose_maps[int(len(env.tumor_images) / 2)][0])
save_tumor_image(env.tumor_images[int(len(env.tumor_images) * 2 / 3)][1], env.tumor_images[int(len(env.tumor_images) * 2 / 3)][0])
save_dose_map(env.dose_maps[int(len(env.tumor_images) * 2 / 3)][1], env.dose_maps[int(len(env.tumor_images) * 2 / 3)][0])
save_tumor_image(env.tumor_images[-1][1], env.tumor_images[-1][0])
save_dose_map(env.dose_maps[-1][1], env.dose_maps[-1][0])
ticks4 = [env.tumor_images[0][0], env.tumor_images[int(len(env.tumor_images) / 3)][0], env.tumor_images[int(len(env.tumor_images) *2 / 3)][0], env.tumor_images[-1][0]]
make_img(ticks4, args.fname+'4')
ticks3 = [env.tumor_images[0][0], env.tumor_images[int(len(env.tumor_images) / 2)][0], env.tumor_images[-1][0]]
make_img3(ticks3, args.fname+'3')


ticks, counts, doses = env.dataset
fig, ax1 = plt.subplots()

color = 'tab:red'
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
plt.savefig('tmp/'+args.fname+'_treat.pdf', format='pdf')


#print(ticks, doses)
plt.clf()
plt.cla()
env.dose_map = None
doses_data = np.full((1000, 200), 0.0, dtype=float)
for i in range(1000):
    env.init_dataset()
    agent._runEpisode(100000)
    _, _, doses = env.dataset
    doses_data[i, :len(doses)] = doses

np.save(args.fname+'_treatments', doses_data)
means = np.nanmean(doses_data, 0)
errs = np.nanstd(doses_data, 0)
counts = np.count_nonzero(~np.isnan(doses_data), 0)
with open('eval/'+args.fname+".csv", 'w') as f:
    f.write('count, mean, std_error\n')
    for i in range(len(counts)):
        if counts[i] == 0:
            break
        else:
            f.write(str(counts[i])+", "+str(means[i])+", "+str(errs[i])+"\n")
steps = [i * (24 if args.network == 'DQN' else 12) for i in range(len(means))]
treatment_var(means, errs, steps, args.fname)

env.end()
