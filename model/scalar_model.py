from math import exp, log, ceil, floor
import matplotlib.pyplot as plt
from model.cell import CancerCell, HealthyCell, OARCell
import random
import numpy as np

alpha_tumor = 0.3
beta_tumor = 0.03
alpha_norm_tissue = 0.15
beta_norm_tissue = 0.03


class ScalarModel:

    def __init__(self, reward, draw=False):
        self.reward = reward
        self.draw_graph = draw
        self.cells = []

    def reset(self):
        del self.cells
        HealthyCell.cell_count = 0
        CancerCell.cell_count = 0
        self.time = 0
        self.cells = [CancerCell(0)] + [HealthyCell(0) for _ in range(1000)]
        self.glucose = 250000
        self.oxygen = 2500000
        if self.draw_graph:
            self.ccell_counts = [CancerCell.cell_count]
            self.hcell_counts = [HealthyCell.cell_count]
            self.ticks = [self.time]
        self.go(350)
        self.init_hcell_count = HealthyCell.cell_count

    def cycle_cells(self):
        to_add = []
        count = HealthyCell.cell_count + CancerCell.cell_count
        for cell in random.sample(self.cells, count):
            res = cell.cycle(self.glucose, count / 278 , self.oxygen)
            if len(res) > 2:  # If there are more than two arguments, a new cell must be created
                if res[2] == 0:  # Mitosis of a healthy cell
                    to_add.append(HealthyCell(0))
                elif res[2] == 1:
                    to_add.append(CancerCell(0))
            self.glucose -= res[0]  # The local variables are updated according to the cell's consumption
            self.oxygen -= res[1]
        self.cells = [cell for cell in self.cells if cell.alive] + to_add

    def fill_sources(self):
        self.glucose += 13000
        self.oxygen += 450000

    def go(self, ticks=1):
        for _ in range(ticks):
            self.time += 1
            self.fill_sources()
            self.cycle_cells()
            #graph
            if self.draw_graph:
                self.ticks.append(self.time)
                self.ccell_counts.append(CancerCell.cell_count)
                self.hcell_counts.append(HealthyCell.cell_count)

    def irradiate(self, dose):
        for cell in self.cells:
            cell.radiate(dose)
        self.cells = [cell for cell in self.cells if cell.alive]

    def observe(self):
        return HealthyCell.cell_count, CancerCell.cell_count

    def act(self, action):
        dose = action + 1
        pre_hcell = HealthyCell.cell_count
        pre_ccell = CancerCell.cell_count
        self.irradiate(dose)
        m_hcell = HealthyCell.cell_count
        m_ccell = CancerCell.cell_count
        self.go(24)
        post_hcell = HealthyCell.cell_count
        post_ccell = CancerCell.cell_count
        return self.adjust_reward(dose, pre_ccell - post_ccell, pre_hcell-min(post_hcell, m_hcell))

    def adjust_reward(self, dose, ccell_killed, hcells_lost):
        if self.inTerminalState():
            if self.end_type == "L" or self.end_type == "T":
                return -1
            else:
                if self.reward == 'dose':
                    return - dose / 200.0 + 0.5 + HealthyCell.cell_count / 4000.0
                else:
                    return 0.5 + HealthyCell.cell_count / 4000.0
        else:
            if self.reward == 'dose' or self.reward == 'oar':
                return - dose / 200.0 + (ccell_killed - 5.0 * hcells_lost) / 100000.0
            elif self.reward == 'killed':
                return  (ccell_killed - int(self.reward) * hcells_lost)/100000.0

    def inTerminalState(self):
        if CancerCell.cell_count <= 0 :
            self.end_type = 'W'
            return True
        elif HealthyCell.cell_count < 10:
            self.end_type = "L"
            return True
        elif self.time > 1550:
            self.end_type = "T"
            return True
        else:
            return False

    def draw(self, title):
        plt.plot(self.ticks, self.ccell_counts, 'r', label='Cancer cells')
        plt.plot(self.ticks, self.hcell_counts, 'b', label='Healthy cells')
        #plt.yscale('log')
        plt.xlabel('Hours')
        plt.ylabel("Count")
        plt.legend()
        plt.title(title)
        plt.savefig(''.join(title.lower().split()))


class TabularLearner:

    def __init__(self, env, cancer_cell_stages, healthy_cell_stages, actions, state_type):
        self.env = env
        self.cancer_cell_stages = cancer_cell_stages
        self.healthy_cell_stages = healthy_cell_stages
        self.actions = actions
        self.state_type = state_type
        self.Q = np.zeros((cancer_cell_stages, healthy_cell_stages, actions), dtype=float)
        if (state_type == 'o'): #log
            self.state_helper_hcells = exp(log(3500.0) / (healthy_cell_stages - 2.0))
            self.state_helper_ccells = exp(log(40000.0) / (cancer_cell_stages - 2.0))
        else: # lin
            self.state_helper_hcells = 3500.0 / (healthy_cell_stages - 2.0)
            self.state_helper_ccells = 40000.0 / (cancer_cell_stages - 2.0)

    def ccell_state(self, count):
        if (self.state_type == 'o'): # log
            return min(self.cancer_cell_stages - 1, int(ceil(log(CancerCell.cell_count + 1) / log(self.state_helper_ccells))))
        else:
            return min(self.cancer_cell_stages - 1, int(ceil(CancerCell.cell_count / self.state_helper_ccells)))


    def hcell_state(self, count):
        if (self.state_type == 'o'): # log
            return min(self.healthy_cell_stages - 1, ceil(log(max(HealthyCell.cell_count -8, 1) ) / log(self.state_helper_hcells)))
        else:
            return min(self.healthy_cell_stages - 1, int(ceil(max(HealthyCell.cell_count - 9, 0) / self.state_helper_hcells)))

    def convert(self, obs):
        return self.ccell_state(obs[1]), self.hcell_state(obs[0])

    def choose_action(self, state, epsilon):
        if random.random() < epsilon:
            return random.randint(0, self.actions - 1)
        else:
            return np.argmax(self.Q[state])

    def train(self, steps, alpha, epsilon, disc_factor):
        self.env.reset()
        while steps > 0:
            while not self.env.inTerminalState() and steps > 0:
                state = self.convert(self.env.observe())
                action = self.choose_action(state, epsilon)
                r = self.env.act(action)
                new_state = self.convert(self.env.observe())
                self.Q[state][action] = (1 - alpha) * self.Q[state][action] + alpha * (r + disc_factor * np.max(self.Q[new_state]))
                steps -= 1
            if steps > 0:
                self.env.reset()


    def test(self, episodes, disc_factor, verbose=False, eval=False):
        sum_scores = 0.0
        sum_error = 0.0
        lengths_arr = []
        fracs_arr = []
        doses_arr = []
        sum_w = 0
        survivals_arr = []
        for _ in range(episodes):
            self.env.reset()
            sum_r = 0
            err = 0.0
            count = 0
            fracs = 0
            doses = 0
            time = 0
            init_hcell = HealthyCell.cell_count
            while not self.env.inTerminalState():
                state = self.convert(self.env.observe())
                action = np.argmax(self.Q[state])
                r = self.env.act(action)
                if verbose:
                    print(action + 1, "grays, reward =", r)
                fracs += 1
                doses += action + 1
                time += 24
                sum_r += r
                new_state = self.convert(self.env.observe())
                err += pow(r + disc_factor * self.Q[new_state][action] - self.Q[state][action], 2.0)
                count += 1
            if verbose:
                print(self.env.end_type)
            if self.env.end_type == 'W':
                sum_w += 1
            if eval:
                fracs_arr.append(fracs)
                doses_arr.append(doses)
                lengths_arr.append(time)
                survival = HealthyCell.cell_count / init_hcell
                survivals_arr.append(survival)
            sum_scores += sum_r
            sum_error += err / count
        fracs_arr = np.array(fracs_arr)
        doses_arr = np.array(doses_arr)
        lengths_arr = np.array(lengths_arr)
        survivals_arr = np.array(survivals_arr)
        print("Average score:", sum_scores / episodes, "MSE:", sum_error / episodes)
        if eval:
            print("TCP: " , 100.0 *sum_w /episodes)
            print("Average num of fractions: ", np.mean(fracs_arr), " std dev: ", np.std(fracs_arr))
            print("Average radiation dose: ", np.mean(doses_arr), " std dev: ", np.std(doses_arr))
            print("Average duration: ", np.mean(lengths_arr), " std dev: ", np.std(lengths_arr))
            print("Average survival: ", np.mean(survivals_arr), " std dev: ", np.std(survivals_arr))


    def run(self, n_epochs, train_steps, test_steps, init_alpha, alpha_mult, init_epsilon, final_epsilon, disc_factor):
        self.test(test_steps, disc_factor)
        alpha = init_alpha
        epsilon = init_epsilon
        epsilon_change = (init_epsilon - final_epsilon) / (n_epochs - 1)
        alpha_change = (init_alpha - alpha_mult) / (n_epochs - 1)
        for i in range(n_epochs):
            print("Epoch ", i + 1)
            self.train(train_steps, alpha, epsilon, disc_factor)
            self.test(test_steps, disc_factor)
            alpha -= alpha_change
            epsilon -= epsilon_change

    def save_Q(self, name):
        np.save(name, self.Q, allow_pickle=False)

    def load_Q(self, name):
        self.Q = np.load(name+'.npy', allow_pickle=False)


random.seed(1234)
env = ScalarModel('killed', draw=True)
env.reset()
env.irradiate(15)
print(HealthyCell.cell_count, CancerCell.cell_count)
env.go()
env.draw('Single dose')
'''
agent = TabularLearner(env, 50, 5, 4)
agent.run(20, 2500, 100, 0.8, 0.5, 0.8, 0.05, 0.95)
agent.save_Q("Qvalkilled")
agent.test(100, verbose=True)
env = ScalarModel('dose')
agent = TabularLearner(env, 50, 5, 4)
agent.run(20, 2500, 100, 0.8, 0.5, 0.8, 0.05, 0.95)
agent.save_Q("Qvaldose")
agent.test(100, verbose=True)
'''




