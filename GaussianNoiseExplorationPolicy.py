from deer.base_classes import Policy
from numpy.random import normal
import numpy as np


class GaussianNoiseExplorationPolicy(Policy):
    def __init__(self, learning_algo, n_actions, random_state, std_dev):
        Policy.__init__(self, learning_algo, n_actions, random_state)
        self._nActions = n_actions
        self._std_dev = std_dev
        self._factors = np.array([(hb-lb) / 2.0 for lb, hb in self._nActions], dtype=np.float)

    def action(self, state, mode=None, *args, **kwargs):
        action, V = self.bestAction(state, mode, *args, **kwargs)
        action += normal(0.0, self._factors * self._std_dev)
        for i in range(len(action)):
            action[i] = self._clip(action[i], self._nActions[i][0], self._nActions[i][1])
        return action, V

    def _clip(self, action, lb, hb):
        if action > hb:
            return hb
        elif action < lb:
            return lb
        else:
            return action

    def setStdDev(self, s):
        self._std_dev = s

    def stdDev(self):
        return self._std_dev

    def epsilon(self):
        """ Get the epsilon for :math:`\epsilon`-greedy exploration
        """
        return self._std_dev
